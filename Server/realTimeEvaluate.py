import os
import numpy as np
from pose import Pose, Part, PoseSequence

def tooMuchRotation(upper_arm_torso_angles):
    return np.median(upper_arm_torso_angles[-10:]) > 35

def notHighEnough(upper_arm_forearm_angles):
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
    
    return tooMuchRotation(upper_arm_torso_angles), notHighEnough(upper_arm_forearm_angles)
        
    
    