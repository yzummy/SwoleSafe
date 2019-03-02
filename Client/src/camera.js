import * as posenet from "@tensorflow-models/posenet";
import React from "react";
import ReactDOM from "react-dom";
import { drawBoundingBox, drawKeypoints, drawSkeleton } from "./demo_util";
import axios from "axios";
import { red } from "ansi-colors";

const warnMsgStyle = {
  color: red
};

const videoWidth = 600;
const videoHeight = 500;
var count1 = 0;
var count2 = 0;
var warn1 = document.getElementById("warning1");
var warn2 = document.getElementById("warning2");

async function setupCamera() {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    throw new Error(
      "Browser API navigator.mediaDevices.getUserMedia not available"
    );
  }

  const video = document.getElementById("video");
  video.width = videoWidth;
  video.height = videoHeight;

  const stream = await navigator.mediaDevices.getUserMedia({
    audio: false,
    video: {
      facingMode: "user",
      width: videoWidth,
      height: videoHeight
    }
  });
  video.srcObject = stream;

  return new Promise(resolve => {
    video.onloadedmetadata = () => {
      resolve(video);
    };
  });
}

async function loadVideo() {
  const video = await setupCamera();
  video.play();
  return video;
}

const guiState = {
  algorithm: "single-pose",
  input: {
    mobileNetArchitecture: "1.01",
    outputStride: 8,
    imageScaleFactor: 0.3
  },
  singlePoseDetection: {
    minPoseConfidence: 0.4,
    minPartConfidence: 0.4
  },
  multiPoseDetection: {
    maxPoseDetections: 5,
    minPoseConfidence: 0.15,
    minPartConfidence: 0.1,
    nmsRadius: 30.0
  },
  output: {
    showVideo: true,
    showSkeleton: true,
    showPoints: true,
    showBoundingBox: false
  },
  net: null
};

function setupGui(cameras, net) {
  guiState.net = net;

  if (cameras.length > 0) {
    guiState.camera = cameras[0].deviceId;
  }
}

function detectPoseInRealTime(video, net) {
  const canvas = document.getElementById("output");
  const ctx = canvas.getContext("2d");
  const flipHorizontal = true;

  canvas.width = videoWidth;
  canvas.height = videoHeight;

  async function poseDetectionFrame() {
    if (guiState.changeToArchitecture) {
      guiState.net.dispose();

      guiState.net = await posenet.load(+guiState.changeToArchitecture);

      guiState.changeToArchitecture = null;
    }

    const imageScaleFactor = guiState.input.imageScaleFactor;
    const outputStride = +guiState.input.outputStride;

    let poses = [];
    let minPoseConfidence;
    let minPartConfidence;
    switch (guiState.algorithm) {
      case "single-pose":
        const pose = await guiState.net.estimateSinglePose(
          video,
          imageScaleFactor,
          flipHorizontal,
          outputStride
        );

        poses.push(pose);
        if (
          pose.score > 0.4 &&
          pose.keypoints[11].score > 0.2 &&
          pose.keypoints[12].score > 0.2 &&
          pose.keypoints[5].score > 0.2 &&
          pose.keypoints[6].score > 0.2 &&
          pose.keypoints[0].score > 0.2
        ) {
          const p = JSON.stringify(pose);
          console.log(p);
          const blob = new Blob([p], {
            type: "application/json"
          });
          const data = new FormData();
          data.append("pose", blob);

          axios.post("http://127.0.0.1:5002/poseup", data).then(response => {
            console.log(response.data);
            if (response.data.tooMuchRotation === 1) {
              ReactDOM.render(
                <AdviceMessage
                  content={
                    "Your upper arm shows too much rotation! Try hold the upper arm still!"
                  }
                />,
                Warn1
              );
              count1 = 20;
            } else {
              if (count1 == 0) {
                ReactDOM.render(
                  <AdviceMessage content={"汪汪汪汪汪汪汪汪汪"} />,
                  Warn1
                );
              } else {
                count1 -= 1;
              }
            }

            if (response.data.notHighEnough === 1) {
              ReactDOM.render(
                <AdviceMessage content={"Curl higher!!!"} />,
                Warn2
              );
              count2 = 20;
            } else {
              if (count2 == 0) {
                ReactDOM.render(
                  <AdviceMessage content={"臭狗狗臭狗狗臭狗狗"} />,
                  Warn2
                );
              } else {
                count2 -= 1;
              }
            }
          });
        }
        minPoseConfidence = +guiState.singlePoseDetection.minPoseConfidence;
        minPartConfidence = +guiState.singlePoseDetection.minPartConfidence;
        break;
      case "multi-pose":
        poses = await guiState.net.estimateMultiplePoses(
          video,
          imageScaleFactor,
          flipHorizontal,
          outputStride,
          guiState.multiPoseDetection.maxPoseDetections,
          guiState.multiPoseDetection.minPartConfidence,
          guiState.multiPoseDetection.nmsRadius
        );

        minPoseConfidence = +guiState.multiPoseDetection.minPoseConfidence;
        minPartConfidence = +guiState.multiPoseDetection.minPartConfidence;
        break;
    }

    ctx.clearRect(0, 0, videoWidth, videoHeight);

    if (guiState.output.showVideo) {
      ctx.save();
      ctx.scale(-1, 1);
      ctx.translate(-videoWidth, 0);
      ctx.drawImage(video, 0, 0, videoWidth, videoHeight);
      ctx.restore();
    }

    poses.forEach(({ score, keypoints }) => {
      if (score >= minPoseConfidence) {
        if (guiState.output.showPoints) {
          drawKeypoints(keypoints, minPartConfidence, ctx);
        }
        if (guiState.output.showSkeleton) {
          drawSkeleton(keypoints, minPartConfidence, ctx);
        }
        if (guiState.output.showBoundingBox) {
          drawBoundingBox(keypoints, ctx);
        }
      }
    });

    requestAnimationFrame(poseDetectionFrame);
  }

  poseDetectionFrame();
}

export async function bindPage() {
  const net = await posenet.load(0.75);

  document.getElementById("loading").style.display = "none";
  document.getElementById("main").style.display = "block";

  let video;

  try {
    video = await loadVideo();
  } catch (e) {
    let info = document.getElementById("info");
    info.textContent =
      "this browser does not support video capture," +
      "or this device does not have a camera";
    info.style.display = "block";
    throw e;
  }

  setupGui([], net);
  detectPoseInRealTime(video, net);
}

navigator.getUserMedia =
  navigator.getUserMedia ||
  navigator.webkitGetUserMedia ||
  navigator.mozGetUserMedia;
bindPage();

class AdviceMessage extends React.Component {
  render() {
    return (
      <div>
        <h1>Caution: {this.props.content}</h1>
      </div>
    );
  }
}

let Warn1 = document.getElementById("warning1");
let Warn2 = document.getElementById("warning2");
