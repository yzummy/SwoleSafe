import React, { Component } from 'react';
import ReactDOM from 'react-dom';

import {
    Button, Modal, Form, Input, Radio, Icon
} from 'antd';
// import axios from 'axios';
import QuesForm from '../QuesForm/QuesForm'
import './MyModal.css'

const FormItem = Form.Item;

class MyModal extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            visible: false,
            name: "mf",
        }
        this.showModal = this.showModal.bind(this);
        this.handleCancel = this.handleCancel.bind(this);
    }
    showModal() {
        this.setState({ visible: true });
    }

    handleCancel() {
        this.setState({ visible: false });
    }


    saveFormRef(formRef) {
        this.formRef = formRef;
    }

    render() {
        const { name } = this.state
        return (
            <div>
                <Button type="primary" onClick={this.showModal}>Start Building Your Own Workout Routine</Button>
                <Modal 
                    className="profileModal"
                    title="Build your profile"
                    visible={this.state.visible}
                    onCancel={this.handleCancel}
                    width="900">
                    <QuesForm
                        name={name}
                    />
                </Modal>
            </div>
        );
    }
}

const modalContainer = document.getElementById("modal");
ReactDOM.render(<MyModal />, modalContainer);

//   export default WrappedRegistrationFrom;