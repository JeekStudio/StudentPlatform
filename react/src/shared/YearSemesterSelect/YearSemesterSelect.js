import React from 'react';
import {Select, Button} from "antd";
import * as PropTypes from 'prop-types';

import Provider from '../../utils/provider';

import './style.scss'

const { Option } = Select;

class YearSemesterSelect extends React.Component {
    state = {
        yearOptions: []
    };

    componentDidMount() {
        Provider.get('/api/manage/settings/')
            .then((res) => {
                let years = new Array(res.data.year - 2018)
                    .fill('')
                    .map((_, index) => {
                        return res.data.year - index
                    });
                this.setState({ yearOptions: years });
            })
            .catch((err) => {
                throw err;
            })
    }

    render() {
        return (
            <div className="year-semester-select">
                <Select
                    value={this.props.year}
                    className="year-select"
                >
                    {
                        this.state.yearOptions.map((option) => (
                            <Option value={option} key={option}>{option}学年</Option>
                        ))
                    }
                </Select>
                <Select
                    className="semester-select"
                    value={this.props.semester}
                >
                    <Option value="1" key="1">第一学期</Option>
                    <Option value="2" key="2">第二学期</Option>
                </Select>
                <Button
                    onClick={() => this.props.searchButtonOnClick}
                    htmlType="button"
                    className="search-button"
                    type="primary"
                >
                    查询
                </Button>
            </div>
        )
    }
}

YearSemesterSelect.propTypes = {
    yearOnChange: PropTypes.func,
    semesterOnChange: PropTypes.func,
    semester: PropTypes.number.isRequired,
    year: PropTypes.number.isRequired,
    searchButtonOnClick: PropTypes.func.isRequired
};

export default YearSemesterSelect;