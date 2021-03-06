import React, { FormEvent } from 'react';
import {Form, Icon, Input, Button, notification, Modal} from 'antd';
import H from 'history';
import Provider from '../../../utils/provider';
import {withRouter} from "react-router-dom";
import {match} from 'react-router';
import PropTypes from "prop-types";
import AccountStore from '../../../shared/stores/AccountStore';
import { AxiosResponse } from 'axios';
import { FormComponentProps } from 'antd/lib/form';


interface LoginFormProps extends FormComponentProps {
    match: match,
    location: H.Location,
    history: H.History,
}

class LoginForm extends React.Component<LoginFormProps, any> {
    redirectWithUserType = () => {
        if (AccountStore.is_student) {
            this.props.history.push('/')
        } else if (AccountStore.is_society) {
            this.props.history.push('/admin_society')
        } else if (AccountStore.is_society_bureau) {
            this.props.history.push('/manage')
        }
    };

    handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        this.props.form.validateFields((err: Error, values: {username: String, password: String}) => {
            if (!err) {
                Provider.post('/api/account/login/', {
                    username: values.username,
                    password: values.password
                }).then((res: AxiosResponse) => {
                    if (res.status === 200) {
                        AccountStore.fetch().then(() => {
                            console.table(AccountStore.user);
                            this.redirectWithUserType();
                            if (!AccountStore.user.password_changed) {
                                Modal.confirm({
                                    title: '温馨提示',
                                    content: '您还未修改过默认密码，账号有被盗用的风险，建议您尽快修改密码！',
                                    okText: '去修改',
                                    cancelText: '算了',
                                    onOk: () => {
                                        if (AccountStore.is_student) {
                                            this.props.history.push('/password')
                                        } else if (AccountStore.is_society) {
                                            this.props.history.push('/admin_society/password')
                                        } else if (AccountStore.is_society_bureau) {
                                            this.props.history.push('/manage/password')
                                        }
                                    }
                                });
                            }
                        });
                    }
                }).catch((err: Error) => {
                    notification.error({
                        message: '登录失败',
                        description: '用户名或密码错误'
                    });
                    console.log(err)
                })
            }
        });
    };

    componentDidMount() {
        if (AccountStore.authenticated) {
            this.redirectWithUserType()
        }
    }

    render() {
        const {getFieldDecorator} = this.props.form;
        return (
            <Form onSubmit={(e) => this.handleSubmit(e)}>
                <Form.Item>
                    {getFieldDecorator('username', {
                        rules: [{required: true, message: '请输入用户名'}],
                    })(
                        <Input size="large" prefix={<Icon type="user" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               placeholder="请输入用户名"/>
                    )}
                </Form.Item>
                <Form.Item>
                    {getFieldDecorator('password', {
                        rules: [{required: true, message: '请输入密码'}],
                    })(
                        <Input size="large" prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               type="password"
                               placeholder="密码"/>
                    )}
                </Form.Item>
                <Form.Item>
                    <Button size="large" type="primary" htmlType="submit" style={{width: '100%'}}>
                        登录
                    </Button>
                </Form.Item>
            </Form>
        )
    }
}

const WrappedLoginForm = Form.create<LoginFormProps>({name: 'student_login'})(LoginForm);

export default withRouter(WrappedLoginForm);