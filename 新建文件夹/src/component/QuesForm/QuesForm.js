import React, { Component } from "react";
import ReactDOM from "react-dom";
import {
  BrowserRouter as Router,
  Route,
  Redirect,
  Link,
  withRouter
} from "react-router-dom";
import axios from "axios";
import logo from "../../../Images/SwoleSafe-logo.png";
// import {
//   Form, Input, Tooltip, Icon, Cascader, Select, Row, Col, Checkbox, Button, AutoComplete,
// } from 'antd';
// import Input from '../../component/input/Input';
import { Radio } from "antd";
import { Slider, InputNumber } from "antd";
const RadioGroup = Radio.Group;
import "antd/dist/antd.css";
import "./QuesForm.css";
import {
  Form,
  Input,
  Tooltip,
  Icon,
  Cascader,
  Select,
  Row,
  Col,
  Checkbox,
  Button,
  AutoComplete
} from "antd";
function hasErrors(fieldsError) {
  return Object.keys(fieldsError).some(field => fieldsError[field]);
}
class QuesForm extends React.Component {
  constructor(props) {
    super(props);
    // Don't call this.setState() here!
    this.state = {
      selectValue: 1,
      inputValue: 22,
      level: "beginner"
    };
    this.onChange = this.onChange.bind(this);
    this.onChangeSlider = this.onChangeSlider.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleLevelChange = this.handleLevelChange.bind(this);
    this.postForm = this.postForm.bind(this);
  }
  componentDidMount() {
    // To disabled submit button at the beginning.
    this.props.form.validateFields();
  }
  onChange(e) {
    this.setState({
      value: e.target.value
    });
  }
  onChangeSlider(sliderValue) {
    console.log("hi");
    console.log(sliderValue);
    this.setState({
      inputValue: sliderValue
    });
  }
  handleLevelChange(value) {
    this.setState({
      level: value
    });
  }
  handleSubmit(e) {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        console.log("Received values of form: ", values.username);
        const formSubmit = this.postForm(
          values.username,
          values.password,
          values.selectMultiple,
          values.level
        );
        console.log("Received values of form: ", values);
      }
    });
  }
  postForm(user, password, bodyparts, level) {
    try {
      return axios
        .post("http://35.184.165.218/users/", {
          username: user,
          password: password,
          bodypart: bodyparts,
          level: level
        })
        .then(() => {
          sessionStorage.setItem("username", user);
          location.href = "/camera.html";
        });
    } catch (error) {
      console.log(error);
    }
  }
  render() {
    const { getFieldDecorator } = this.props.form;
    const { inputValue } = this.state;
    return (
      <Form onSubmit={this.handleSubmit} className="login-form">
        <div className="blueBox box">
          <img src={logo} className="logo" />
          <Row>
            <Col span={10}>
              <Form.Item label="Name" className="flexCon">
                {getFieldDecorator("username", {
                  // rules: [{ required: true, message: 'Please input your username!' }],
                })(
                  <Input
                    prefix={
                      <Icon type="user" style={{ color: "rgba(0,0,0,.25)" }} />
                    }
                    placeholder="Username"
                  />
                )}
              </Form.Item>
            </Col>
            <Col span={10}>
              <Form.Item label="Password" className="flexCon">
                {getFieldDecorator("password", {
                  // rules: [{ required: true, message: 'Please input your Password!' }],
                })(
                  <Input
                    prefix={
                      <Icon type="key" style={{ color: "rgba(0,0,0,.25)" }} />
                    }
                    placeholder="Password"
                  />
                )}
              </Form.Item>
            </Col>
          </Row>
        </div>
        <div className="pinkBox box">
          <Form.Item label="Gender" className="flexCon">
            {getFieldDecorator("radiobox-group", {})(
              <RadioGroup
                onChange={this.onChange}
                value={this.state.selectValue}
              >
                <Radio value={1}>Female</Radio>
                <Radio value={2}>Male</Radio>
              </RadioGroup>
            )}
          </Form.Item>
          <Form.Item label="Age" className="flexCon age-container">
            {getFieldDecorator("rslider", {})(
              <Row>
                <Col span={10}>
                  <Slider
                    min={0}
                    max={100}
                    onChange={this.onChangeSlider}
                    // value={typeof inputValue === 'number' ? inputValue : 0}
                    value={inputValue}
                  />
                </Col>
                <Col span={10}>
                  <InputNumber
                    min={0}
                    max={100}
                    style={{ marginLeft: 16 }}
                    value={inputValue}
                    onChange={this.onChangeSlider}
                  />
                  {/* yrs */}
                </Col>
              </Row>
            )}
          </Form.Item>
          <Row>
            <Col span={10}>
              <Form.Item label="Height" className="flexCon">
                {getFieldDecorator("height", {})(
                  <div>
                    <Input
                      prefix={
                        <Icon
                          type="height"
                          style={{ color: "rgba(0,0,0,.25)" }}
                        />
                      }
                      placeholder="Height"
                    />
                    {/* ft */}
                  </div>
                )}
              </Form.Item>
            </Col>
            <Col span={10}>
              <Form.Item label="Weight" className="flexCon">
                {getFieldDecorator("weight", {})(
                  <div>
                    <Input
                      prefix={
                        <Icon
                          type="weight"
                          style={{ color: "rgba(0,0,0,.25)" }}
                        />
                      }
                      placeholder="Weight"
                    />
                    {/* <span> lbs</span> */}
                  </div>
                )}
              </Form.Item>
            </Col>
          </Row>
        </div>
        <div className="greenBox box">
          <Form.Item label="Level" className="flexCon">
            {getFieldDecorator("level", {})(
              <Select
                defaultValue="beginner"
                style={{ width: 120 }}
                onChange={this.handleLevelChange}
              >
                <Option value="beginner">Beginner</Option>
                <Option value="intermediate">Intermediate</Option>
                <Option value="advanced">Advanced</Option>
              </Select>
            )}
          </Form.Item>
          <Form.Item label="Bodypart" className="flexCon">
            {getFieldDecorator("selectMultiple", {})(
              <Select
                mode="multiple"
                placeholder="Please select body part you want to work on"
              >
                <Option value="biceps">Biceps</Option>
                <Option value="abs">Abs</Option>
                <Option value="deltoids">Deltoids</Option>
                <Option value="hamstrings">Ham Strings</Option>
                <Option value="quadriceps">Quadriceps</Option>
                <Option value="triceps">Triceps</Option>
                <Option value="back">Back</Option>
                <Option value="glutes">Glutes</Option>
                <Option value="chest">Chest</Option>
                <Option value="forearms">Forearms</Option>
              </Select>
            )}
          </Form.Item>
        </div>
        <Form.Item className="signUpBtn">
          <Button type="primary" htmlType="submit" className="sign-up">
            Submit
          </Button>
        </Form.Item>
      </Form>
    );
  }
}
const WrappedQuesForm = Form.create({ name: "signup" })(QuesForm);
// const quesContainer = document.getElementById("ques");
// ReactDOM.render(<WrappedRegistrationForm />, quesContainer);
export default WrappedQuesForm;
