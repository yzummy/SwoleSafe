import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Loading from '../Loading/Loading';
import {
    Button, Modal, Form, Input, Radio, Icon
} from 'antd';
// import axios from 'axios';
import QuesForm from '../QuesForm/QuesForm'
import './SugModal.css'

const FormItem = Form.Item;

class SugModal extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            visible: false,
            name: "mf",
            loading: true,
            visibleResult: false
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

    componentDidMount() {
        setTimeout(() => { this.setState({ loading: !this.state.loading, visibleResult: !this.state.visibleResult }) }, 5000);
      }

    render() {
        const { name } = this.state
        const {loading} = this.state
        const {visibleResult} = this.state
        return (
            <div>
                <Button type="primary" onClick={this.showModal}>Start Building Your Own Workout Routine</Button>
                <Modal 
                    className="suggestModal"
                    title="Good Job Working Out!"
                    visible={this.state.visible}
                    onCancel={this.handleCancel}
                    width="900">
                    {/* <QuesForm
                        name={name}
                    /> */}
                    <Loading loading={loading}></Loading>
                    {/* <div className="result" visible={visibleResult}>ert</div> */}
                    {!this.state.visibleResult && (<div>ert</div>)}
                </Modal>
            </div>
        );
    }
}

const modalContainer = document.getElementById("sugBtn");
ReactDOM.render(<SugModal />, modalContainer);

//   export default WrappedRegistrationFrom;