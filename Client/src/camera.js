import * as posenet from "@tensorflow-models/posenet";
import React from "react";
import ReactDOM from "react-dom";
import { drawBoundingBox, drawKeypoints, drawSkeleton } from "./demo_util";
import axios from "axios";
import { red } from "ansi-colors";
import { Tabs, Progress } from "antd";

import "antd/dist/antd.css";
import "../CSS/ListEx.css";
import bicep_curl from "../Images/bicep_curl.gif";
import front_raise from "../Images/front_raise.gif";
import squat from "../Images/squat.gif";
import push_up from "../Images/push_up.gif";
const warnMsgStyle = {
  color: red
};

const videoWidth = 500;
const videoHeight = 400;
var count1 = 0;
var count2 = 0;
var currentExercise = 1;
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

          axios
            .post(
              "http://127.0.0.1:5002/" + demos[currentExercise - 1].request,
              data
            )
            .then(response => {
              console.log(response.data);
              if (response.data.e1 === 1) {
                ReactDOM.render(
                  <AdviceMessage content={response.data.warn0} />,
                  Warn1
                );
                count1 = 20;
              } else {
                if (count1 == 0) {
                  ReactDOM.render(
                    <AdviceMessage content={"You are doing great!"} />,
                    Warn1
                  );
                } else {
                  count1 -= 1;
                }
              }

              if (response.data.e2 === 1) {
                ReactDOM.render(
                  <AdviceMessage content={response.data.warn1} />,
                  Warn2
                );
                count2 = 20;
              } else {
                if (count2 == 0) {
                  ReactDOM.render(
                    <AdviceMessage content={"Keep up!"} />,
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
        <h1 className="warn">Caution: {this.props.content}</h1>
      </div>
    );
  }
}

let Warn1 = document.getElementById("warning1");
let Warn2 = document.getElementById("warning2");

let listEx = document.getElementById("listEx");
const TabPane = Tabs.TabPane;

function changeTab(key) {
  console.log("clicked detect ", key, demos[key - 1]);
  currentExercise = key;
}
var demos = [
  {
    index: 1,
    name: "Bicep Curl",
    number: 10,
    gif: bicep_curl,
    request: "bicepCurl"
  },
  {
    index: 2,
    name: "Front Raise",
    number: 10,
    gif: front_raise,
    request: "frontRaise"
  },
  { index: 3, name: "Squat", number: 10, gif: squat, request: "deepSquat" },
  { index: 4, name: "Pushup", number: 10, gif: push_up, request: "pushUp" }
];
var demos_populated = [];
function generateList() {
  axios
    .get("http://35.184.165.218/recommendation/3", {
      headers: {
        "Access-Control-Allow-Origin": "*"
      }
    })
    .then(response => {
      JSON.parse(response.data).forEach(item => {
        switch (item.exercise) {
          case "Front Raise":
            demos[1].number = item.length;
            demos_populated.push(demos[1]);
            break;
          case "Bicep Curl":
            demos[0].number = item.length;
            demos_populated.push(demos[0]);
            break;
          case "Squat":
            demos[2].number = item.length;
            demos_populated.push(demos[2]);
            break;
          case "Pushup":
            demos[3].number = item.length;
            demos_populated.push(demos[3]);
            break;
        }
        console.log(demos, demos_populated);
      });

      ReactDOM.render(
        <Tabs
          defaultActiveKey="1"
          tabPosition="left"
          style={{ height: "400px" }}
          onChange={changeTab}
        >
          {demos_populated.map(demo => (
            <TabPane
              tab={demo.name + " (" + String(demo.number) + "x)"}
              key={demo.index}
            >
              <img src={demo.gif} className="center" />
            </TabPane>
          ))}
        </Tabs>,

        listEx
      );
    });
}
generateList();
