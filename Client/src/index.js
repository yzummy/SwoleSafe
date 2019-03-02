import React from "react";
import ReactDOM from "react-dom";

const app = document.getElementById("app");
const btn = document.getElementById("btn");

function ActionLink() {
  function onclick() {
    console.log("The link was clicked.");
    location.href = "/camera.html";
    console.log("The address was clicked.");
  }

  return (
    <button onClick={onclick} type="button">
      Camera
    </button>
  );
}
ReactDOM.render(<ActionLink />, btn);
