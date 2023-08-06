"""
To improve performance assertions could be commented
uncomment to test and comment for deployment
TODO:
    Write Docstring
    Add logger for exceptions
    Add type hints
"""

from typing import Dict

import cv2
import numpy as np
import torch

from iai_common.communications.isp import Action as isp_Action
from iai_common.communications.isp import BoundingBox as isp_BoundingBox
from iai_common.communications.isp import ClientHandshake as isp_ClientHandshake
from iai_common.communications.isp import Command as isp_Command
from iai_common.communications.isp import Dict as isp_Dict
from iai_common.communications.isp import Info as isp_Info
from iai_common.communications.isp import Initialize as isp_Initialize
from iai_common.communications.isp import Location as isp_Location
from iai_common.communications.isp import Message as isp_Message
from iai_common.communications.isp import MessageBody as isp_MessageBody
from iai_common.communications.isp import Obs as isp_Obs
from iai_common.communications.isp import Resolution as isp_Resolution
from iai_common.communications.isp import Rotation as isp_Rotation
from iai_common.communications.isp import Sensor as isp_Sensor
from iai_common.communications.isp import SensorData as isp_SensorData
from iai_common.communications.isp import SensorsDataDict as isp_SensorsDataDict
from iai_common.communications.isp import SensorsDict as isp_SensorsDict
from iai_common.communications.isp import ServerHandshake as isp_ServerHandshake
from iai_common.communications.isp import State as isp_State
from iai_common.communications.isp import Step as isp_Step
from iai_common.communications.isp import Tensor as isp_Tensor
from iai_common.communications.isp import WorldParameters as isp_WorldParameters
from iai_common.communications.isp import ScenarioParameters as isp_ScenarioParameters
import collections

Resolution = collections.namedtuple('Resolution', ['width', 'height'])

class Res:
    """
    Some commonly used resolutions.
    """
    DEFAULT = Resolution(1280, 720)
    CIL = Resolution(200, 88)
    BIRDVIEW = Resolution(256, 256)
    SD = Resolution(640, 480)
    MD = Resolution(320, 240)

class SensorSettings:
    Available_Sensors = ['camera']
    Available_Camera_types = ['rgb-camera', 'segmentation', 'depth-camera']
    Location = collections.namedtuple('Location', ['x', 'y', 'z'])
    Rotation = collections.namedtuple('Rotation', ['yaw', 'pitch', 'roll'])
    Resolution = collections.namedtuple('Resolution', ['width', 'height'])
    Available_Tracked_Actors = ['vehicles', 'pedestrians', 'traffic-lights', 'parked_vehicles']
    Available_Reference_Frame = ['carla']  # 'opendrive', 'geolocation' will be added
    Default_Settings = {
        'camera': {
            'sensor_type': 'camera',
            'camera_type': 'rgb-camera',
            'bounding_box': True,
            'track_actor_types': Available_Tracked_Actors,  # or 'all'
            'show_bounding_boxes': True,
            'world_sensor': False,
            'location': Location(x=1.6, z=1.7, y=0),
            'rotation': Rotation(yaw=0, pitch=0, roll=0),
            'resolution': Resolution(200, 88),
            'fov': 90.0,
        },
        'boundingbox': {
            'sensor_type': 'boundingbox',
            'track_actor_types': Available_Tracked_Actors,  # or 'all'
            'world_sensor': False,
            'location': Location(x=0, z=0, y=0),
            'rotation': Rotation(yaw=0, pitch=0, roll=0),
            'frame_of_reference': 'carla',
            # if world_sensor=True returns coordinated based on either 'carla', 'opendrive', 'geolocation'
            'attach_to_actor': 'ego',
            'radius': 100000,  # If not specified all world is considered
            'occlusion': False,
        },
    }


def get_message_body(message_buffer):
    message = isp_Message.Message.GetRootAsMessage(message_buffer, 0)
    body_type = message.BodyType()
    if body_type == isp_MessageBody.MessageBody().ServerHandshake:
        message_body = isp_ServerHandshake.ServerHandshake()
        message_body.Init(message.Body().Bytes, message.Body().Pos)
        system_name = message_body.SystemName().decode("utf-8")
        model_name = message_body.ModelName().decode("utf-8")
        return "ServerHandshake", (system_name, model_name)
    elif body_type == isp_MessageBody.MessageBody().ClientHandshake:
        message_body = isp_ClientHandshake.ClientHandshake()
        message_body.Init(message.Body().Bytes, message.Body().Pos)
        return "ClientHandshake", (message_body.SystemName().decode("utf-8"))
    elif body_type == isp_MessageBody.MessageBody().Tensor:
        message_body = isp_Tensor.Tensor()
        message_body.Init(message.Body().Bytes, message.Body().Pos)
        data = message_body.DataAsNumpy()
        shape = message_body.ShapeAsNumpy()
        return "Tensor", (data.reshape(shape))
    elif body_type == isp_MessageBody.MessageBody().Command:
        message_body = isp_Command.Command()
        message_body.Init(message.Body().Bytes, message.Body().Pos)
        return "Command", unpack_command(message_body)
    elif body_type == isp_MessageBody.MessageBody().Initialize:
        message_body = isp_Initialize.Initialize()
        message_body.Init(message.Body().Bytes, message.Body().Pos)
        return "Initialize", unpack_initialize(message_body)
    elif body_type == isp_MessageBody.MessageBody().Dict:
        message_body = isp_Dict.Dict()
        message_body.Init(message.Body().Bytes, message.Body().Pos)
        return "Dict", unpack_dict(message_body)
    elif body_type == isp_MessageBody.MessageBody().Obs:
        message_body = isp_Obs.Obs()
        message_body.Init(message.Body().Bytes, message.Body().Pos)
        return "Obs", unpack_obs(message_body)
    elif body_type == isp_MessageBody.MessageBody().State:
        message_body = isp_State.State()
        message_body.Init(message.Body().Bytes, message.Body().Pos)
        return "State", unpack_state(message_body)
    elif body_type == isp_MessageBody.MessageBody().SensorsDict:
        message_body = isp_SensorsDict.SensorsDict()
        message_body.Init(message.Body().Bytes, message.Body().Pos)
        return "Sensors", unpack_sensors_dict(message_body)
    elif body_type == isp_MessageBody.MessageBody().SensorsDataDict:
        message_body = isp_SensorsDataDict.SensorsDataDict()
        message_body.Init(message.Body().Bytes, message.Body().Pos)
        return "Sensors_Data", unpack_sensor_data_dict(message_body)
    else:
        raise RuntimeError(
            "isp (Python):\
            Received unexpected message body type: {}".format(body_type)
        )


def build_message(builder, message_body, body_type):
    isp_Message.MessageStart(builder)
    isp_Message.MessageAddBodyType(builder,
                                   body_type)
    isp_Message.MessageAddBody(builder, message_body)
    message = isp_Message.MessageEnd(builder)
    builder.Finish(message)
    return builder.Output()


def build_clienthandshake(builder, system_name):
    assert type(system_name) == str
    system_name = builder.CreateString(system_name)
    isp_ClientHandshake.ClientHandshakeStart(builder)
    isp_ClientHandshake.ClientHandshakeAddSystemName(builder, system_name)

    # return = isp_ClientHandshake.ClientHandshakeEnd(builder)
    message_body = isp_ClientHandshake.ClientHandshakeEnd(builder)
    return build_message(builder, message_body,
                         isp_MessageBody.MessageBody().ClientHandshake)


def build_serverhandshake(builder, system_name, model_name):
    assert type(system_name) == str
    assert type(model_name) == str
    system_name = builder.CreateString(system_name)
    model_name = builder.CreateString(model_name)
    isp_ServerHandshake.ServerHandshakeStart(builder)
    isp_ServerHandshake.ServerHandshakeAddSystemName(builder, system_name)
    isp_ServerHandshake.ServerHandshakeAddModelName(builder, model_name)
    message_body = isp_ServerHandshake.ServerHandshakeEnd(builder)
    return build_message(builder, message_body,
                         isp_MessageBody.MessageBody().ServerHandshake)


def build_tensor(builder, data: np.ndarray, get_as_message=False):
    assert ((type(data) == np.ndarray) or
            (type(data) == np.matrix))
    shape = list(data.shape)
    data = np.asarray(data).flatten().tolist()
    # pack data
    isp_Tensor.TensorStartDataVector(builder, len(data))
    for d in reversed(data):
        builder.PrependFloat64(d)
    data = builder.EndVector()
    # pack shape
    isp_Tensor.TensorStartShapeVector(builder, len(shape))
    for s in reversed(shape):
        builder.PrependInt32(s)
    shape = builder.EndVector()
    isp_Tensor.TensorStart(builder)
    isp_Tensor.TensorAddData(builder, data)
    isp_Tensor.TensorAddShape(builder, shape)
    if get_as_message:
        message_body = isp_Tensor.TensorEnd(builder)
        return build_message(builder, message_body,
                             isp_MessageBody.MessageBody().Tensor)
    else:
        return isp_Tensor.TensorEnd(builder)


def unpack_tensor(message_body):
    data = message_body.DataAsNumpy()
    shape = message_body.ShapeAsNumpy()
    return data.reshape(shape)


def build_dict(builder, in_dict: Dict, get_as_message=False):
    encoded_keys = []
    encoded_values = []
    for key in in_dict.keys():
        encoded_keys.append(builder.CreateString(key))
    for value in in_dict.values():
        encoded_values.append(build_tensor(builder, value))

    isp_Dict.DictStartKeysVector(builder, len(in_dict))
    for key in reversed(encoded_keys):
        builder.PrependUOffsetTRelative(key)
    serialized_keys = builder.EndVector()
    isp_Dict.DictStartValuesVector(builder, len(in_dict))
    for value in reversed(encoded_values):
        builder.PrependUOffsetTRelative(value)
    serialized_values = builder.EndVector()

    isp_Dict.DictStart(builder)
    isp_Dict.DictAddKeys(builder, serialized_keys)
    isp_Dict.DictAddValues(builder, serialized_values)
    if get_as_message:
        message_body = isp_Dict.DictEnd(builder)
        return build_message(builder, message_body,
                             isp_MessageBody.MessageBody().Dict)
    else:
        return isp_Dict.DictEnd(builder)


def unpack_dict(message_body):
    decoded_keys = []
    decoded_values = []
    for l in range(message_body.KeysLength()):
        decoded_keys.append(message_body.Keys(l).decode())
        decoded_values.append(unpack_tensor(message_body.Values(l)))
    decoded_dict = {decoded_keys[i]: decoded_values[i]
                    for i in range(message_body.KeysLength())}
    return decoded_dict


def build_command(builder, cmd, data=None):
    if data is None:
        data = {}
    command_text = builder.CreateString(cmd)
    if 'tensor' in data.keys():
        packed_tensor = build_tensor(builder, data['tensor'])
    if 'step' in data.keys():
        packed_step = build_step(builder, data['step'])
    isp_Command.CommandStart(builder)
    isp_Command.CommandAddCmd(builder, command_text)
    if 'tensor' in data.keys():
        isp_Command.CommandAddTensorArgs(builder, packed_tensor)
    if 'step' in data.keys():
        isp_Command.CommandAddStep(builder, packed_step)
    message_body = isp_Command.CommandEnd(builder)
    return build_message(builder, message_body,
                         isp_MessageBody.MessageBody().Command)


def unpack_command(message_body):
    cmd = message_body.Cmd().decode("utf-8")
    body = {}
    if message_body.TensorArgs() is not None:
        data = message_body.TensorArgs().DataAsNumpy()
        shape = message_body.TensorArgs().ShapeAsNumpy()
        body['tensor'] = data.reshape(shape)
    if message_body.Step() is not None:
        body['step'] = unpack_step(message_body.Step())
    return cmd, body


def build_initialize(builder, scenario, scenario_parameters=None,
                     world_parameters=None, vehicle_physics=None,
                     sensors=None):
    scenario_name = builder.CreateString(scenario)
    if scenario_parameters is not None:
        isp_ScenarioParameters.ScenarioParametersStart(builder)
        if scenario_parameters['camera_location_variation'] is not None:
            isp_ScenarioParameters.ScenarioParametersAddCameraLocationVariation(builder, isp_Location.CreateLocation(
                builder, scenario_parameters['camera_location_variation'].x,
                scenario_parameters['camera_location_variation'].y, scenario_parameters['camera_location_variation'].z))
        if scenario_parameters['camera_rotation_variation'] is not None:
            isp_ScenarioParameters.ScenarioParametersAddCameraOrientationVariation(builder, isp_Rotation.CreateRotation(
                builder, scenario_parameters['camera_rotation_variation'].yaw,
                scenario_parameters['camera_rotation_variation'].roll,
                scenario_parameters['camera_rotation_variation'].pitch))
        scenarioparam = isp_ScenarioParameters.ScenarioParametersEnd(builder)
    if vehicle_physics is not None:
        pass
    if world_parameters is not None:
        if 'carlatown' in world_parameters:
            carlatown = builder.CreateString(world_parameters['carlatown'])
        isp_WorldParameters.WorldParametersStart(builder)
        if 'carlatown' in world_parameters:
            isp_WorldParameters.WorldParametersAddCarlatown(builder, carlatown)
        if 'traffic_count' in world_parameters:
            isp_WorldParameters.WorldParametersAddTrafficCount(builder, world_parameters['traffic_count'])
        if 'pedestrian_count' in world_parameters:
            isp_WorldParameters.WorldParametersAddPedestrianCount(builder, world_parameters['pedestrian_count'])
        worldparam = isp_WorldParameters.WorldParametersEnd(builder)
    if sensors is not None:
        serialized_sensors = build_sensor_dict(builder, sensors, get_as_message=False)
    isp_Initialize.InitializeStart(builder)
    isp_Initialize.InitializeAddScenario(builder, scenario_name)
    if scenario_parameters is not None:
        isp_Initialize.InitializeAddScenarioParameters(builder, scenarioparam)
    if vehicle_physics is not None:
        pass
    if world_parameters is not None:
        isp_Initialize.InitializeAddWorldParameters(builder, worldparam)
    if sensors is not None:
        isp_Initialize.InitializeAddSensors(builder, serialized_sensors)
    message_body = isp_Initialize.InitializeEnd(builder)
    return build_message(builder, message_body,
                         isp_MessageBody.MessageBody().Initialize)


def unpack_initialize(message_body):
    scenario = message_body.Scenario().decode("utf-8")
    world_parameters = None
    sensors = None
    vehicle_physics = None
    scenario_parameters = None
    if message_body.WorldParameters() is not None:
        world_parameters = {}
        if message_body.WorldParameters().Carlatown() is not None:
            world_parameters['carlatown'] = message_body.WorldParameters().Carlatown().decode("utf-8")
        if message_body.WorldParameters().TrafficCount() is not None:
            world_parameters['traffic_count'] = message_body.WorldParameters().TrafficCount()
        if message_body.WorldParameters().PedestrianCount() is not None:
            world_parameters['pedestrian_count'] = message_body.WorldParameters().PedestrianCount()
    if message_body.ScenarioParameters() is not None:
        scenario_parameters = {}
        if message_body.ScenarioParameters().CameraLocationVariation() is not None:
            scenario_parameters['camera_location_variation'] = SensorSettings.Location(
                x=message_body.ScenarioParameters().CameraLocationVariation().X(),
                z=message_body.ScenarioParameters().CameraLocationVariation().Z(),
                y=message_body.ScenarioParameters().CameraLocationVariation().Y())
        if message_body.ScenarioParameters().CameraOrientationVariation() is not None:
            scenario_parameters['camera_rotation_variation'] = SensorSettings.Rotation(
                yaw=message_body.ScenarioParameters().CameraOrientationVariation().Yaw(),
                pitch=message_body.ScenarioParameters().CameraOrientationVariation().Pitch(),
                roll=message_body.ScenarioParameters().CameraOrientationVariation().Roll())
    if message_body.Sensors() is not None:
        sensors = unpack_sensors_dict(message_body.Sensors())
    body = {'scenario': scenario, 'world_parameters': world_parameters,
            'vehicle_physics': vehicle_physics,
            'scenario_parameters': scenario_parameters, 'sensors': sensors}
    return body


def build_obs(builder, obs: Dict, get_as_message: bool = False, compress=True):
    """
    speed: float front_image: torch.Tensor
    birdview_image: torch.Tensor, command: str,
    compact_vector: np.ndarray, prev_action: tuple,
    """
    command = builder.CreateString(obs['command'])

    if compress:
        im = (obs['front_image'].squeeze().permute(1, 2, 0).numpy() * 255).astype(np.uint8)
        img_encode = cv2.imencode('.jpg', im)[1].reshape([-1, 1])
        front_image = build_tensor(builder, img_encode)
        im = (obs['birdview_image'].squeeze().permute(1, 2, 0).numpy() * 255).astype(np.uint8)
        img_encode = cv2.imencode('.jpg', im)[1].reshape([-1, 1])
        birdview_image = build_tensor(builder, img_encode)
    else:
        front_image = build_tensor(builder, obs['front_image'].numpy())
        birdview_image = build_tensor(builder, obs['birdview_image'].numpy())
    compact_vector = build_tensor(builder, obs['compact_vector'])
    if 'sensor_data' in obs.keys():
        sensor_data = build_sensor_data_dict(builder, obs['sensor_data'])
    # prev_action = build_tensor(builder, np.array(obs['prev_action']))
    isp_Obs.ObsStart(builder)
    isp_Obs.ObsAddSpeed(builder, obs['speed'])
    isp_Obs.ObsAddFrontImage(builder, front_image)
    isp_Obs.ObsAddBirdviewImage(builder, birdview_image)
    isp_Obs.ObsAddCommand(builder, command)
    isp_Obs.ObsAddCompactVector(builder, compact_vector)
    isp_Obs.ObsAddPrevAction(builder, isp_Action.CreateAction(
        builder, obs['prev_action'][0], obs['prev_action'][1]))
    if 'sensor_data' in obs.keys():
        isp_Obs.ObsAddSensorData(builder, sensor_data)
    message_body = isp_Obs.ObsEnd(builder)
    if get_as_message:
        return build_message(builder, message_body,
                             isp_MessageBody.MessageBody().Obs)
    else:
        return message_body


def unpack_obs(message_body, compress=True):
    obs = {}
    obs['speed'] = message_body.Speed()
    if compress:
        rec_im = unpack_tensor(message_body.FrontImage()).astype(np.uint8).squeeze()
        obs['front_image'] = cv2.imdecode(rec_im, cv2.IMREAD_COLOR)
        rec_im = unpack_tensor(message_body.BirdviewImage()).astype(np.uint8).squeeze()
        obs['birdview_image'] = cv2.imdecode(rec_im, cv2.IMREAD_COLOR)
    else:
        obs['front_image'] = torch.Tensor(unpack_tensor(message_body.FrontImage()).copy())
        obs['birdview_image'] = torch.Tensor(unpack_tensor(message_body.BirdviewImage()).copy())
    obs['command'] = message_body.Command().decode()
    obs['compact_vector'] = unpack_tensor(message_body.CompactVector())
    obs['prev_action'] = (message_body.PrevAction().Acceleration(),
                          message_body.PrevAction().Steering())
    if message_body.SensorData() is not None:
        obs['sensor_data'] = unpack_sensor_data_dict(message_body.SensorData())
    return obs


def build_info(builder, info: Dict):
    """
      invasion: bool;
      collision: bool;
      gear: int;
      expert_action: isp_Action;
      outcome: Tensor;                  // TODO: Not sure what it should be
      next_waypoint_distance: float;
      distance_to_goal: float;
      waypoints_found: int;
      waypoints_total: int;
      waypoints_remaining: int;
   """
    outcome = build_tensor(builder, info['outcome'])

    isp_Info.InfoStart(builder)
    isp_Info.InfoAddInvasion(builder, info['invasion'])
    isp_Info.InfoAddCollision(builder, info['collision'])
    isp_Info.InfoAddGear(builder, info['gear'])
    isp_Info.InfoAddExpertAction(builder, isp_Action.CreateAction(
        builder, info['expert_action'][0], info['expert_action'][1]))
    isp_Info.InfoAddOutcome(builder, outcome)
    if 'next_waypoint_distance' in info.keys():
        isp_Info.InfoAddNextWaypointDistance(builder, info['next_waypoint_distance'])
    if 'distance_to_goal' in info.keys():
        isp_Info.InfoAddDistanceToGoal(builder, info['distance_to_goal'])
    if 'waypoints_found' in info.keys():
        isp_Info.InfoAddWaypointsFound(builder, info['waypoints_found'])
    if 'waypoints_total' in info.keys():
        isp_Info.InfoAddWaypointsTotal(builder, info['waypoints_total'])
    if 'waypoints_remaining' in info.keys():
        isp_Info.InfoAddWaypointsRemaining(builder, info['waypoints_remaining'])
    return isp_Info.InfoEnd(builder)


def unpack_info(message_body):
    info = {'invasion': message_body.Invasion(), 'collision': message_body.Collision(), 'gear': message_body.Gear(),
            'expert_action': (message_body.ExpertAction().Acceleration(),
                              message_body.ExpertAction().Steering()), 'outcome': unpack_tensor(message_body.Outcome()),
            'next_waypoint_distance': message_body.NextWaypointDistance(),
            'distance_to_goal': message_body.DistanceToGoal(), 'waypoints_found': message_body.WaypointsFound(),
            'waypoints_total': message_body.WaypointsTotal(), 'waypoints_remaining': message_body.WaypointsRemaining()}
    return info


def build_state(builder, obs, reward, done, info):
    packed_obs = build_obs(builder, obs)
    packed_info = build_info(builder, info)
    isp_State.StateStart(builder)
    isp_State.StateAddObs(builder, packed_obs)
    isp_State.StateAddReward(builder, reward)
    isp_State.StateAddDone(builder, done)
    isp_State.StateAddInfo(builder, packed_info)
    message_body = isp_State.StateEnd(builder)
    return build_message(builder, message_body,
                         isp_MessageBody.MessageBody().State)


def unpack_state(message_body):
    obs = unpack_obs(message_body.Obs())
    reward = message_body.Reward()
    done = message_body.Done()
    info = unpack_info(message_body.Info())
    return {'obs': obs, 'reward': reward, 'done': done, 'info': info}


def build_step(builder, action):
    isp_Step.StepStart(builder)
    isp_Step.StepAddAction(builder, isp_Action.CreateAction(builder, action[0],
                                                            action[1]))
    return isp_Step.StepEnd(builder)


def unpack_step(message_body):
    action = (message_body.Action().Acceleration(),
              message_body.Action().Steering())
    return action


def build_sensor(builder, sensor_name: str, sensor: Dict):
    name = builder.CreateString(sensor_name)
    sensor_type = builder.CreateString(sensor['sensor_type'])
    if 'camera_type' in sensor.keys():
        camera_type = builder.CreateString(sensor['camera_type'])
    if 'track_actor_types' in sensor.keys():
        track_actor_types = []
        for actor in sensor['track_actor_types']:
            track_actor_types.append(builder.CreateString(actor))
        isp_Sensor.SensorStartTrackActorTypesVector(builder, len(track_actor_types))
        for actor in reversed(track_actor_types):
            builder.PrependUOffsetTRelative(actor)
        serialized_actor = builder.EndVector()
    if 'attach_to_actor' in sensor.keys():
        attach_to_actor = builder.CreateString(sensor['attach_to_actor'])
    if 'frame_of_reference' in sensor.keys():
        frame_of_reference = builder.CreateString(sensor['frame_of_reference'])

    isp_Sensor.SensorStart(builder)
    isp_Sensor.SensorAddSensorName(builder, name)
    isp_Sensor.SensorAddSensorTypes(builder, sensor_type)
    if 'camera_type' in sensor.keys():
        isp_Sensor.SensorAddCameraType(builder, camera_type)
    if 'bounding_box' in sensor.keys():
        isp_Sensor.SensorAddBoundingBox(builder, sensor['bounding_box'])
    if 'track_actor_types' in sensor.keys():
        isp_Sensor.SensorAddTrackActorTypes(builder, serialized_actor)
    if 'show_bounding_boxes' in sensor.keys():
        isp_Sensor.SensorAddShowBoundingBoxes(builder, sensor['show_bounding_boxes'])
    if 'world_sensor' in sensor.keys():
        isp_Sensor.SensorAddWorldSensor(builder, sensor['world_sensor'])
    if 'location' in sensor.keys():
        isp_Sensor.SensorAddSensorLocation(builder, isp_Location.CreateLocation(
            builder, sensor['location'].x, sensor['location'].y, sensor['location'].z))
    if 'rotation' in sensor.keys():
        isp_Sensor.SensorAddSensorRotation(builder, isp_Rotation.CreateRotation(
            builder, sensor['rotation'].yaw, sensor['rotation'].roll, sensor['rotation'].pitch))
    if 'resolution' in sensor.keys():
        isp_Sensor.SensorAddSensorResolution(builder, isp_Resolution.CreateResolution(
            builder, sensor['resolution'].width, sensor['resolution'].height))
    if 'radius' in sensor.keys():
        isp_Sensor.SensorAddRadius(builder, sensor['radius'])
    if 'fov' in sensor.keys():
        isp_Sensor.SensorAddFov(builder, sensor['fov'])
    if 'attach_to_actor' in sensor.keys():
        isp_Sensor.SensorAddAttachToActor(builder, attach_to_actor)
    if 'frame_of_reference' in sensor.keys():
        isp_Sensor.SensorAddFrameOfReference(builder, frame_of_reference)
    if 'occlusion' in sensor.keys():
        isp_Sensor.SensorAddOcclusion(builder, sensor['occlusion'])

    return isp_Sensor.SensorEnd(builder)


def unpack_sensor(message_body):
    sensor = {}
    name = message_body.SensorName().decode("utf-8")
    sensor['sensor_type'] = message_body.SensorTypes().decode("utf-8")
    if message_body.CameraType() is not None:
        sensor['camera_type'] = message_body.CameraType().decode("utf-8")
    if message_body.BoundingBox() is not None:
        sensor['bounding_box'] = message_body.BoundingBox()
    if not message_body.TrackActorTypesIsNone():
        track_actor_types = []
        for l in range(message_body.TrackActorTypesLength()):
            track_actor_types.append(message_body.TrackActorTypes(l).decode())
        sensor['track_actor_types'] = track_actor_types
    if message_body.ShowBoundingBoxes() is not None:
        sensor['show_bounding_boxes'] = message_body.ShowBoundingBoxes()
    if message_body.WorldSensor() is not None:
        sensor['world_sensor'] = message_body.WorldSensor()
    if message_body.SensorResolution() is not None:
        sensor['resolution'] = SensorSettings.Resolution(
            width=message_body.SensorResolution().Width(),
            height=message_body.SensorResolution().Height())
    if message_body.SensorLocation() is not None:
        sensor['location'] = SensorSettings.Location(
            x=message_body.SensorLocation().X(),
            z=message_body.SensorLocation().Z(),
            y=message_body.SensorLocation().Y())
    if message_body.SensorRotation() is not None:
        sensor['rotation'] = SensorSettings.Rotation(
            yaw=message_body.SensorRotation().Yaw(),
            pitch=message_body.SensorRotation().Pitch(),
            roll=message_body.SensorRotation().Roll())
    if message_body.Fov() != 0.0:
        sensor['fov'] = message_body.Fov()
    if message_body.Radius() != 0.0:
        sensor['radius'] = message_body.Radius()
    if message_body.FrameOfReference() is not None:
        sensor['frame_of_reference'] = message_body.FrameOfReference().decode("utf-8")
    if message_body.AttachToActor() is not None:
        sensor['attach_to_actor'] = message_body.AttachToActor().decode("utf-8")
    if message_body.Occlusion() is not None:
        sensor['occlusion'] = message_body.Occlusion()
    return name, sensor


def build_sensor_dict(builder, sensors_dict: Dict, get_as_message=False):
    sensor_array = []
    for sensor in sensors_dict:
        sensor_array.append(build_sensor(
            builder, sensor, sensors_dict[sensor]))
    isp_SensorsDict.SensorsDictStartSensorsVector(builder, len(sensor_array))
    for sensor in reversed(sensor_array):
        builder.PrependUOffsetTRelative(sensor)
    serialized_sensor = builder.EndVector()
    isp_SensorsDict.SensorsDictStart(builder)
    isp_SensorsDict.SensorsDictAddSensors(builder, serialized_sensor)
    if get_as_message:
        message_body = isp_SensorsDict.SensorsDictEnd(builder)
        return build_message(builder, message_body,
                             isp_MessageBody.MessageBody().SensorsDict)
    else:
        return isp_SensorsDict.SensorsDictEnd(builder)


def unpack_sensors_dict(message_body):
    sensors_dict = {}
    for l in range(message_body.SensorsLength()):
        name, sns = unpack_sensor(message_body.Sensors(l))
        sensors_dict[name] = sns
    return sensors_dict


def build_sensor_data(builder, sensor_name: str, data: Dict, get_as_message=False, compress=True):
    name = builder.CreateString(sensor_name)
    no_id_bbox = None
    bbox = None
    image = None
    for key in data:
        if key == 'image':
            if compress:
                img_encode = cv2.imencode('.jpg', data[key])[1].reshape([-1, 1])
                image = build_tensor(builder, img_encode)
            else:
                image = build_tensor(builder, data[key])
        elif key == 'bounding_boxes':
            bbox = []
            for actor in data[key]:
                bbox.append(build_bounding_box(builder, actor, data[key][actor]))
            pass
        elif key == 'no_id_bounding_boxes':
            for actor in data[key].keys():
                data[key][actor] = np.array(data[key][actor])
            no_id_bbox = build_dict(builder, data[key])
        else:
            raise RuntimeError(
                "isp (Python):\
                unexpected sensor data type: {}".format(key))

    if bbox is not None:
        isp_SensorData.SensorDataStartBoundingBoxVector(builder, len(bbox))
        for box in bbox:
            builder.PrependUOffsetTRelative(box)
        serialized_bbox = builder.EndVector()

    isp_SensorData.SensorDataStart(builder)
    isp_SensorData.SensorDataAddSensorName(builder, name)
    if image is not None:
        isp_SensorData.SensorDataAddImage(builder, image)
    if bbox is not None:
        isp_SensorData.SensorDataAddBoundingBox(builder, serialized_bbox)
    return isp_SensorData.SensorDataEnd(builder)


def unpack_sensor_data(message_body, compress=True):
    sensor_data = {}
    name = message_body.SensorName().decode("utf-8")
    if message_body.Image() is not None:
        if compress:
            rec_im = unpack_tensor(message_body.Image()).astype(np.uint8).squeeze()
            im = cv2.imdecode(rec_im, cv2.IMREAD_COLOR)
            sensor_data['image'] = im
        else:
            sensor_data['image'] = unpack_tensor(message_body.Image())
    if not message_body.BoundingBoxIsNone():
        sensor_data['bounding_boxes'] = {}
        for l in range(message_body.BoundingBoxLength()):
            actor_type, data_list = unpack_bounding_box(message_body.BoundingBox(l))
            sensor_data['bounding_boxes'][actor_type] = data_list
    return name, sensor_data


def build_sensor_data_dict(builder, sensors_data_dict: Dict, get_as_message=False):
    sensor_data_array = []
    for sensor in sensors_data_dict:
        sensor_data_array.append(build_sensor_data(
            builder, sensor, sensors_data_dict[sensor]))
    isp_SensorsDataDict.SensorsDataDictStartSensorsDataVector(builder, len(sensor_data_array))
    for sensor in reversed(sensor_data_array):
        builder.PrependUOffsetTRelative(sensor)
    serialized_sensor_data = builder.EndVector()
    isp_SensorsDataDict.SensorsDataDictStart(builder)
    isp_SensorsDataDict.SensorsDataDictAddSensorsData(builder, serialized_sensor_data)
    message_body = isp_SensorsDataDict.SensorsDataDictEnd(builder)
    if get_as_message:
        return build_message(builder, message_body,
                             isp_MessageBody.MessageBody().SensorsDataDict)
    else:
        return message_body


def unpack_sensor_data_dict(message_body):
    sensors_data_dict = {}
    for i in range(message_body.SensorsDataLength()):
        name, data = unpack_sensor_data(message_body.SensorsData(i))
        sensors_data_dict[name] = data
    return sensors_data_dict


def build_bounding_box(builder, actor_type: str, data_list: Dict):
    name = builder.CreateString(actor_type)
    encoded_ids = []
    encoded_cords = []
    encoded_states = []
    encoded_occlusion = []
    for item_id, item in data_list.items():
        encoded_cords.append(build_tensor(builder, item['cords']))
        encoded_ids.append(int(item_id))
        if 'state' in item.keys():
            encoded_states.append(builder.CreateString(item['state']))
        if 'occlusion' in item.keys():
            encoded_occlusion.append(item['occlusion'])

    isp_BoundingBox.BoundingBoxStartIdsVector(builder, len(encoded_ids))
    for int_id in reversed(encoded_ids):
        builder.PrependUint64(int_id)
    serialized_ids = builder.EndVector()
    isp_BoundingBox.BoundingBoxStartCoordinatesVector(builder, len(encoded_cords))
    for cord in reversed(encoded_cords):
        builder.PrependUOffsetTRelative(cord)
    serialized_cords = builder.EndVector()
    if len(encoded_states) > 0:
        isp_BoundingBox.BoundingBoxStartStateVector(builder, len(encoded_states))
        for cord in reversed(encoded_states):
            builder.PrependUOffsetTRelative(cord)
        serialized_states = builder.EndVector()
    if len(encoded_occlusion) > 0:
        isp_BoundingBox.BoundingBoxStartOcclusionVector(builder, len(encoded_occlusion))
        for ocl in reversed(encoded_occlusion):
            builder.PrependFloat64(ocl)
        serialized_occlusion = builder.EndVector()

    isp_BoundingBox.BoundingBoxStart(builder)
    isp_BoundingBox.BoundingBoxAddActorType(builder, name)
    isp_BoundingBox.BoundingBoxAddIds(builder, serialized_ids)
    isp_BoundingBox.BoundingBoxAddCoordinates(builder, serialized_cords)
    if len(encoded_states) > 0:
        isp_BoundingBox.BoundingBoxAddState(builder, serialized_states)
    if len(encoded_occlusion) > 0:
        isp_BoundingBox.BoundingBoxAddOcclusion(builder, serialized_occlusion)

    return isp_BoundingBox.BoundingBoxEnd(builder)


def unpack_bounding_box(message_body):
    decoded = {}
    actor_type = message_body.ActorType().decode("utf-8")
    for l in range(message_body.IdsLength()):
        decoded_id = message_body.Ids(l)
        decoded_cords = unpack_tensor(message_body.Coordinates(l))
        decoded_state = None
        decoded_occlusion = None
        if not message_body.StateIsNone():
            decoded_state = message_body.State(l).decode("utf-8")
        if not message_body.OcclusionIsNone():
            decoded_occlusion = message_body.Occlusion(l)
        decoded[decoded_id] = {}
        decoded[decoded_id] = {'cords': decoded_cords,
                               'state': decoded_state,
                               'occlusion': decoded_occlusion}
    return actor_type, decoded
