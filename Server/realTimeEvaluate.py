import os
import numpy as np
from pose import Pose, Part, PoseSequence

def tooMuchRotation_bicep_curl(upper_arm_torso_angles):
    return np.median(upper_arm_torso_angles[-10:]) > 35

def notHighEnough_bicep_curl(upper_arm_forearm_angles):
    interval = upper_arm_forearm_angles[-10:]
    minAngle = np.min(interval)
    if minAngle< interval[0] and minAngle < interval[-1]:
        if minAngle > 70:
            return True 
    return False

def _bicep_curl(keypoints):
    pose_seq = PoseSequence(keypoints)
    
    # find the arm that is seen most consistently
    poses = pose_seq.poses
    right_present = [1 for pose in poses 
            if pose.rshoulder.exists and pose.relbow.exists and pose.rwrist.exists]
    left_present = [1 for pose in poses
            if pose.lshoulder.exists and pose.lelbow.exists and pose.lwrist.exists]
    right_count = sum(right_present)
    left_count = sum(left_present)
    side = 'right' if right_count > left_count else 'left'

    print('Exercise arm detected as: {}.'.format(side))

    if side == 'right':
        joints = [(pose.rshoulder, pose.relbow, pose.rwrist, pose.rhip, pose.neck) for pose in poses]
    else:
        joints = [(pose.lshoulder, pose.lelbow, pose.lwrist, pose.lhip, pose.neck) for pose in poses]

    # filter out data points where a part does not exist
    joints = [joint for joint in joints if all(part.exists for part in joint)]

    upper_arm_vecs = np.array([(joint[0].x - joint[1].x, joint[0].y - joint[1].y) for joint in joints])
    torso_vecs = np.array([(joint[4].x - joint[3].x, joint[4].y - joint[3].y) for joint in joints])
    forearm_vecs = np.array([(joint[2].x - joint[1].x, joint[2].y - joint[1].y) for joint in joints])

    # normalize vectors
    upper_arm_vecs = upper_arm_vecs / np.expand_dims(np.linalg.norm(upper_arm_vecs, axis=1), axis=1)
    torso_vecs = torso_vecs / np.expand_dims(np.linalg.norm(torso_vecs, axis=1), axis=1)
    forearm_vecs = forearm_vecs / np.expand_dims(np.linalg.norm(forearm_vecs, axis=1), axis=1)

    upper_arm_torso_angles = np.degrees(np.arccos(np.clip(np.sum(np.multiply(upper_arm_vecs, torso_vecs), axis=1), -1.0, 1.0)))
    upper_arm_forearm_angles = np.degrees(np.arccos(np.clip(np.sum(np.multiply(upper_arm_vecs, forearm_vecs), axis=1), -1.0, 1.0)))
    print("upper_arm_torso_angles", upper_arm_torso_angles.shape, upper_arm_torso_angles)
    print("upper_arm_forearm_angles", upper_arm_forearm_angles.shape, upper_arm_forearm_angles)
    
    return tooMuchRotation_bicep_curl(upper_arm_torso_angles), notHighEnough_bicep_curl(upper_arm_forearm_angles)
     
def tooMuchRotation_front_raise(back_vec):
    return np.max(back_vec[-10:], axis=0) - np.min(back_vec[-10:], axis=0) > 0.2

def notHighEnough_front_raise(angles):
    interval = angles[-10:]
    maxAngle = np.max(interval)
    if maxAngle > interval[0] and maxAngle > interval[-1]:
        if maxAngle < 90:
            return True 
    return False

def _front_raise(keypoints):
    pose_seq = PoseSequence(keypoints)
    
    poses = pose_seq.poses
    right_present = [1 for pose in poses 
            if pose.rshoulder.exists and pose.relbow.exists and pose.rwrist.exists]
    left_present = [1 for pose in poses
            if pose.lshoulder.exists and pose.lelbow.exists and pose.lwrist.exists]
    right_count = sum(right_present)
    left_count = sum(left_present)
    side = 'right' if right_count > left_count else 'left'

    if side == 'right':
        joints = [(pose.rshoulder, pose.relbow, pose.rwrist, pose.rhip, pose.neck) for pose in poses]
    else:
        joints = [(pose.lshoulder, pose.lelbow, pose.lwrist, pose.lhip, pose.neck) for pose in poses]

    joints = [joint for joint in joints if all(part.exists for part in joint)]
    joints = np.array(joints)
    
    back_vec = np.array([(joint[4].x - joint[3].x) for joint in joints])

    #back_vec_range = np.max(back_vec, axis=0) - np.min(back_vec, axis=0)

    torso_vecs = np.array([(joint[0].x - joint[3].x, joint[0].y - joint[3].y) for joint in joints])
    arm_vecs = np.array([(joint[0].x - joint[2].x, joint[0].y - joint[2].y) for joint in joints])
    
    torso_vecs = torso_vecs / np.expand_dims(np.linalg.norm(torso_vecs, axis=1), axis=1)
    arm_vecs = arm_vecs / np.expand_dims(np.linalg.norm(arm_vecs, axis=1), axis=1)
    
    angles = np.degrees(np.arccos(np.clip(np.sum(np.multiply(torso_vecs, arm_vecs), axis=1), -1.0, 1.0)))
    
    print("front raise data: ", back_vec, angles)
    
    return tooMuchRotation_front_raise(back_vec), notHighEnough_front_raise(angles)
    
    
    
    
def notParallel(hip_to_knee):
    interval = hip_to_knee[-10:]
    minDiff = np.min(interval)
    if minDiff < interval[0] and minDiff < interval[-1]:
        if minDiff > 0.2:
            return True 
    return False        
    
def tooSeparate(angles):
    interval = angles[-20:]
    medianAngle = np.median(interval)
    if medianAngle > 60:
        return True 
    else:
        return False 

def _squat(keypoints):
    pose_seq = PoseSequence(keypoints) 
    poses = pose_seq.poses
    joints = [( pose.rhip, pose.rknee, pose.rankle, pose.lhip, pose.lhip, pose.lankle) for pose in poses]
    joints = [joint for joint in joints if all(part.exists for part in joint)]
    joints = np.array(joints)   
    hip_to_knee = np.array([np.abs(joint[0].y - joint[1].y) for joint in joints])    
    left_leg_vecs = np.array([(joint[0].x - joint[5].x, joint[0].y - joint[5].y) for joint in joints])
    right_leg_vecs = np.array([(joint[3].x - joint[2].x, joint[3].y - joint[2].y) for joint in joints])    
    angles = np.degrees(np.arccos(np.clip(np.sum(np.multiply(left_leg_vecs, right_leg_vecs), axis=1), -1.0, 1.0)))        
    print("squat data: ", hip_to_knee, angles)
    return notParallel(hip_to_knee), tooSeparate(angles)
    
    
    
    
    
    
def notStraight(body_angle):
    interval = angles[-10:]
    medianAngle = np.median(interval)
    if medianAngle < 150:
        return True 
    else:
        return False 
 
    
def notLowEnough(neck_to_ankle_ydiff):
    interval = hip_to_knee[-10:]
    minDiff = np.min(interval)
    if minDiff < interval[0] and minDiff < interval[-1]:
        if minDiff > 60:
            return True 
    return False       

def _push_up(keypoints):
    pose_seq = PoseSequence(keypoints) 
    poses = pose_seq.poses
    right_present = [1 for pose in poses 
            if pose.rshoulder.exists and pose.relbow.exists and pose.rwrist.exists]
    left_present = [1 for pose in poses
            if pose.lshoulder.exists and pose.lelbow.exists and pose.lwrist.exists]
    right_count = sum(right_present)
    left_count = sum(left_present)
    side = 'right' if right_count > left_count else 'left'

    if side == 'right':
        joints = [(pose.rshoulder, pose.rhip, pose.rankle) for pose in poses]
    else:
        joints = [(pose.lshoulder, pose.lhip, pose.lankle) for pose in poses]

    joints = [joint for joint in joints if all(part.exists for part in joint)]
    joints = np.array(joints)
    

    torso_vecs = np.array([(joint[0].x - joint[1].x, joint[0].y - joint[1].y) for joint in joints])
    leg_vecs = np.array([(joint[1].x - joint[2].x, joint[1].y - joint[2].y) for joint in joints])
    torso_vecs = torso_vecs / np.expand_dims(np.linalg.norm(torso_vecs, axis=1), axis=1)
    leg_vecs = leg_vecs / np.expand_dims(np.linalg.norm(leg_vecs, axis=1), axis=1)
    body_angle = np.degrees(np.arccos(np.clip(np.sum(np.multiply(torso_vecs, arm_vecs), axis=1), -1.0, 1.0)))
    
    
    neck_to_ankle_ydiff = np.array([joint[0].y - joint[2].y for joint in joints ])
    
    
    return notStaight(body_angle), notLowEnough(neck_to_ankle_ydiff)
        
    
    