import React from 'react';
import {Route, Switch} from "react-router-dom";
import Loadable from "react-loadable";
import {Col, Row} from "antd";

import GenericHeader from "./components/GenericHeader";
import Login from "./containers/Login";
import WrappedChangePasswordForm from "../../shared/change_password/ChangePasswordForm";

import {LoginRequiredRoute} from "../../shared/route";
import Loading from "../../shared/Loading";
import NotFound from "../../shared/NotFound/NotFound";
import './styles/SocietyHome.scss';

const Society = Loadable({
    loader: () => import(/* webpackChunkName: "society" */'../society/index.js'),
    loading: Loading,
});

const Activity = Loadable({
    loader: () => import(/* webpackChunkName: "activity" */'./activity/index.js'),
    loading: Loading,
});

const StudentPage = Loadable({
    loader: () => import(/* webpackChunkName: "student-page" */'./containers/StudentPage'),
    loading: Loading,
});

export default function withGenericHeader({match}) {
    return (
        <div className="society-home-container">
            <GenericHeader/>
            <Row className="mt-5" type="flex" justify="space-around">
                <Col xs={22} sm={22} md={20} lg={20} xl={20} xxl={18}>
                    <Switch>
                        <Route path={`${match.url}society`} component={Society}/>
                        <Route path={`${match.url}activity`} component={Activity}/>
                        <Route path={`${match.url}login`} component={Login}/>
                        <LoginRequiredRoute path={`${match.url}password`} component={WrappedChangePasswordForm}/>
                        <LoginRequiredRoute path={`${match.url}student`} component={StudentPage}/>
                        <Route component={NotFound}/>
                    </Switch>
                </Col>
            </Row>
        </div>

    )
}