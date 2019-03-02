import numpy as np
PART_NAMES = ['nose', 'neck',  'rshoulder', 'relbow', 'rwrist', 'lshoulder',
              'lelbow', 'lwrist', 'rhip', 'rknee', 'rankle', 'lhip', 'lknee', 'lankle', 
              'reye', 'leye', 'rear', 'lear']
order = [0,-1,6,8,10,5,7,9,12,14,16,11,13,15,2,1,4,3]

def convert(keypoints):
    poses = []
    for frame in keypoints:
        key = frame['keypoints']
        pose = []
        for o in order:
            if o >= 0:
                part = np.array([key[o]['position']['x'], key[o]['position']['y'], key[o]['score']])
            else:
                part = np.array([key[0]['position']['x'], key[0]['position']['y'], key[0]['score']])
            pose.append(part)
        poses.append(np.array(pose))
    poses = np.array(poses)
    return poses