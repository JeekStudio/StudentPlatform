import React from 'react';
import {Breadcrumb, Row, Col} from 'antd';
import {withRouter, Link} from "react-router-dom";
import PropTypes from 'prop-types';

const breadcrumbNameMap = {
    '/manage': '主页',
    '/manage/profile': '个人信息',
};

class LocationBreadcrumb extends React.Component {
    static propTypes = {
        match: PropTypes.object.isRequired,
        location: PropTypes.object.isRequired,
        history: PropTypes.object.isRequired
    };

    render() {
        const {location} = this.props;
        const pathSnippets = location.pathname.split('/').filter(i => i);
        const extraBreadcrumbItems = pathSnippets.map((_, index) => {
            const url = `/${pathSnippets.slice(0, index + 1).join('/')}`;
            return (
                <Breadcrumb.Item key={url}>
                    <Link to={url}>
                        {breadcrumbNameMap[url]}
                    </Link>
                </Breadcrumb.Item>
            );
        });
        const breadcrumbItems = [].concat(extraBreadcrumbItems);

        return (
            <Row>
                <Col xs={0} sm={0} md={0} lg={24} xl={24}>
                    <Breadcrumb>
                        {breadcrumbItems}
                    </Breadcrumb>
                </Col>
            </Row>
        )
    }
}

export default withRouter(LocationBreadcrumb);