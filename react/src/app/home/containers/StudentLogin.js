import React from 'react';
import WrappedStudentLoginForm from '../components/StudentLoginForm';
import {Row, Col} from 'antd';
import 'bootstrap/scss/bootstrap.scss';

class StudentLogin extends React.Component {
    render() {
        return (
            <div>
                <Row type="flex" justify="center">
                    <Col xl={6} lg={12} md={20}>
                        <Row>
                            <Col>
                                <h2 className="text-center">学生登录</h2>
                            </Col>
                        </Row>
                        <Row>
                            <Col>
                                <WrappedStudentLoginForm/>
                            </Col>
                        </Row>
                    </Col>
                </Row>
            </div>
        )
    }
}

export default StudentLogin;