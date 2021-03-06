import {Component} from "react";
import {Modal, Form, InputNumber} from "antd";
import React from "react";
import * as PropTypes from "prop-types";
import CreditStore from "../stores/CreditStore";

class CreditSetAllModal extends Component {
    render() {
        return (
            <Modal
                visible={CreditStore.setAllModalVisible}
                onCancel={() => CreditStore.setAllModalVisible = false}
                onOk={() => CreditStore.submitSetAllCredit()}
                okText="一键设置！"
                cancelText="算了，下次吧"
            >
                <Form>
                    <Form.Item label="可获得学分的成员人数最大值">
                        <InputNumber
                            value={CreditStore.setAllCredit}
                            onChange={(value) => CreditStore.setAllCredit = value}
                        />
                    </Form.Item>
                </Form>
            </Modal>
        )
    }
}

export default CreditSetAllModal;