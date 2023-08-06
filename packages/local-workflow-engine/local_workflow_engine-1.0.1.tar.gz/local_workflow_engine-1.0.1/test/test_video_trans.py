from asyncio.log import logger
from unittest import result
from asl_workflow_engine.logger import init_logging
from asl_workflow_engine.state_engine import StateEngine
from threading import Timer
from asl_workflow_engine.arn import parse_arn
import json
import unittest
import base64
import redis
import random,string,os
import shutil
import warnings
import re
ASL = """{
  "Comment": "A Hello World example of the Amazon States Language using Pass states",
  "StartAt": "SplitVideo",
  "States": {
    "SplitVideo": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:187983511897:function:SplitVideo",
      "OutputPath":"$$.Execution",
      "ResultPath":"$",
      "Parameters": {
        "Input.$": "$",
        "WorkDir":"test_video_trans_func/SplitVideo"
      },
      "Next": "SegmentalVideoSolution"
    },
    "SegmentalVideoSolution": {
      "Type": "Map",
      "InputPath":"$",
      "ItemsPath": "$.Input.item",
      "ResultPath": "$",
      "Iterator": {
        "StartAt": "VideoSolution",
        "States": {
          "VideoSolution": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:us-east-1:187983511897:function:VideoSolution",
            "Parameters":{
                "WorkDir":"test_video_trans_func/VideoSolution",
                "Dependencies":["SplitVideo"]
            },
            "End": true
          }
        }
      },
      "Next": "ComposeVideo"
    },
    "ComposeVideo": {
      "Type": "Task",
      "InputPath": "$",
      "OutputPath":"$",
      "Resource": "arn:aws:lambda:us-east-1:187983511897:function:ComposeVideo",
      "Parameters":{
        "WorkDir":"test_video_trans_func/ComposeVideo",
        "Dependencies":["VideoSolution"]
      },
      "End": true
    }
  }
}"""
"""
The application context is described in the AWS documentation:
https://docs.aws.amazon.com/step-functions/latest/dg/input-output-contextobject.html 

{
    "Execution": {
        "Id": <String>,
        "Input": <Object>,
        "StartTime": <String Format: ISO 8601>
    },
    "State": {
        "EnteredTime": <String Format: ISO 8601>,
        "Name": <String>,
        "RetryCount": <Number>
    },
    "StateMachine": {
        "Id": <String>,
        "Definition": <Object representing ASL state machine>
    },
    "Task": {
        "Token": <String>
    }
}

The most important paths for state traversal are:
$$.State.Name = the current state
$$.StateMachine.Definition = (optional) contains the complete ASL state machine
$$.StateMachine.Id = a unique reference to an ASL state machine
"""

context = '{"StateMachine": {"Id": "arn:aws:states:local:0123456789:stateMachine:simple_state_machine", "Definition": ' + str(ASL) + '}}'
output_file_key=[]

config = {"workdir":"/test_video_trans_func",
          "preload_data_key":"video.mp4",
          "preload_data_path":"test_video_trans_func/RawData/video.mp4"
          }
state_engine_config = {
            "state_engine": {
                "store_url": "ASL_store.json", 
                "execution_ttl": 500
            }
      }
class Params():
    """Class that loads hyperparameters from a json file.
        Example:
        ```
        params = Params(json_path)
        print(params.learning_rate)
        params.learning_rate = 0.5  # change the value of learning_rate in params
        ```
        """
    def __init__(self, json_path):
        with open(json_path) as f:
            params = json.load(f) 
            self.__dict__.update(params)

    def save(self, json_path):
        with open(json_path, 'w') as f:
            json.dump(self.__dict__, f, indent=4)  

    def update(self, json_path):
        """Loads parameters from json file"""
        with open(json_path) as f:
            params = json.load(f)
            self.__dict__.update(params)

    @property
    def dict(self):
        """Gives dict-like access to Params instance by `params.dict['learning_rate']"""
        return self.__dict__

class EventDispatcherStub(object):

    def __init__(self, state_engine, config):

        """
        Create an association with the state engine and give that a reference
        back to this event dispatcher so that it can publish events and make
        use of the set_timeout time scheduler.
        """
        self.state_engine = state_engine
        self.state_engine.event_dispatcher = self
        self.message_count = -1

    """
    This simple threaded timeout should work OK, the real timeout is actually
    implemented using Pika's connection.call_later() which is single threaded
    and handled within Pika's event loop. That approach plays much better with
    Pika's event loop.
    """
    def set_timeout(self, callback, delay):
        t = Timer(delay/1000, callback)
        t.start()
        return t

    def dispatch(self, message):
        """
        Start at -1 and increment before call to notify as this stub, unlike
        the real EventDispatcher will recursively call dispatch as the State
        Engine calls publish, this means code after the call to notify won't
        be reached when one might expect it to.
        """
        self.message_count += 1
        # The notify method expects a JSON object not a string.
        self.state_engine.notify(json.loads(message), self.message_count)

    def acknowledge(self, id):
        pass

    def publish(self, item):
        # Save Execution StartTime to use when validating output
        if self.message_count == 0:
            self.execution_start_time = item["context"]["Execution"]["StartTime"]
        # Convert event back to JSON string for dispatching.
        self.dispatch(json.dumps(item))

    def broadcast(self, subject, message, carrier_properties=None):
        self.output_event = message

def genRandomString(slen=10):
    return ''.join(random.sample(string.ascii_letters + string.digits, slen))

def get_lower_case_name(text):
    lst = []
    for index, char in enumerate(text):
        if char.isupper() and index != 0:
            lst.append("-")
        lst.append(char)

    return "".join(lst).lower()

def execute_task_stub(resource_arn, parameters, callback,timeout, context):
    
    arn = parse_arn(resource_arn)
    service = arn["service"]  # e.g. rpcmessage, fn, openfaas, lambda
    resource_type = arn["resource_type"]  # Should be function most times
    resource = arn["resource"]  # function-name
    configDir= parameters["WorkDir"]+'/config.json'  
    config_context={
            "resource":resource,
            "service":service,
            "resource_type":resource_type,
            "function_url":"192.168.122.201:31112/function/"+get_lower_case_name(resource)
          }
    if resource=='SplitVideo':
        config_context['dependencies_output_key']=['video.mp4']
    with open(configDir,'w+') as config:
        config.write(json.dumps(config_context))      
    result = {"parameters":parameters,"context":context}
    print(result)     
    callback(result)

def execute_task_openfaas(resource_arn, parameters, callback,timeout, context):
    arn = parse_arn(resource_arn)
    resource = arn["resource"]
    workdir=parameters['WorkDir']
    result = {"parameters":parameters,"Output":context}
    func_dir="test_video_trans_func/"+resource+"/"
    print(func_dir)
    mycopyfile("test_video_trans_func/handler_templete.py",func_dir,"handler.py")
    callback(result)

def execute_openfaas_request(resource_arn, parameters, callback,timeout, context):
    arn = parse_arn(resource_arn)
    resource = arn["resource"]  # function-name
    function_url="192.168.122.201:31112/function/" +get_lower_case_name(resource)
    if "Dependencies" in parameters:
        dependency_key_list=[]
        for i in parameters['Dependencies']:
            with open('test_video_trans_func/'+i+"/config.json","r") as f:
                dependency_func_config=json.loads(f.read())
                try:
                    for i in dependency_func_config['output_key_list']:
                        dependency_key_list.append(i)
                except:
                    print('-------------------error----------------------')
        with open('test_video_trans_func/'+resource+"/config.json","w") as f:
            config={'resource':resource,'arn':arn,"function_url":function_url,'dependency_key_list':dependency_key_list}
            f.write(json.dumps(config))
            if 'Branch' in context['State']:
                index=context['State']['Branch'][0]['Index']
                parameters['dependency_key_list']=[dependency_key_list[0][index]]
                parameters['index']=str(index)
            else:
                parameters['dependency_key_list']=[]
                for i in dependency_key_list:
                    parameters['dependency_key_list'].append(i[0])
    cmd= ''' curl '''+function_url+''' --data '''+"'"+json.dumps(parameters)+"'"
    print("cmd***********************************",cmd)
    result=os.popen(cmd)
    cmd_context=result.read()
    print(cmd_context)
    cmd_list=re.split('\n',cmd_context)
    cmd_return=cmd_list[len(cmd_list)-2]
    cmd_return=cmd_return.replace("'", '"')
    cmd_obj=json.loads(cmd_return)
    function_name = get_lower_case_name(resource)
    output_key_list=cmd_obj['output_key_list']
    with open('test_video_trans_func/'+resource+"/config.json","r+") as f:
        config=json.loads(f.read())
    if('output_key_list' in config and len(config['output_key_list'])>0):
        config['output_key_list'].append(output_key_list)
    else:
        config['output_key_list']=[]
        config['output_key_list'].append(output_key_list)
    with open('test_video_trans_func/'+resource+"/config.json","w+") as f:
        f.write(json.dumps(config))
    result=cmd_obj
    callback(result)
     
def mycopyfile(srcfile,dstpath,fname):                       
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
    else:
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)                                                  
        shutil.copy(srcfile, dstpath + fname)          
        # print ("copy %s -> %s"%(srcfile, dstpath + fname))

class TestVideoTrans(unittest.TestCase):

    def setUp(self):
      # Initialise logger
        logger=init_logging(log_name="function_build_engine")

    def test_get_folder(self):
        state_engine = StateEngine(state_engine_config)
        state_engine.task_dispatcher.execute_task = execute_task_stub
        self.event_dispatcher = EventDispatcherStub(state_engine, config)
        self.event_dispatcher.dispatch('{"data":{"item":[1,2,3]}, "context": ' + context + '}')

    def test_execute_task_openfaas(self):
        state_engine = StateEngine(state_engine_config)
        # Stub out the real TaskDispatcher execute_task
        state_engine.task_dispatcher.execute_task = execute_task_openfaas
        self.event_dispatcher = EventDispatcherStub(state_engine, config)
        self.event_dispatcher.dispatch('{"data":{"item":[1,2,3]}, "context": ' + context + '}')

    def test_async_api(self):
        cmd='cd test_video_trans_func && faas up -f stack.yaml'
        os.system(cmd)
        state_engine = StateEngine(state_engine_config)
        self.event_dispatcher = EventDispatcherStub(state_engine, config)
        state_engine.task_dispatcher.execute_task=execute_openfaas_request
        self.event_dispatcher.dispatch('{"data":{"item":[1,2,3]}, "context": ' + context + '}')
        

if __name__ == '__main__':
    unittest.main()
