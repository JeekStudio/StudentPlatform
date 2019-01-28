import React from 'react';
import {Form, Input} from 'antd';
import {observer} from 'mobx-react';

import SocietyStore from '../stores/SocietyStore'

const Search = Input.Search;

@observer
class SocietySearch extends React.Component {

    handleQueryChange = (e) => {
        e.preventDefault();
        SocietyStore.changeQuery(e.target.value)
    };

    handleSearch = () => {
        SocietyStore.changeLoading();
        console.log(SocietyStore.query);
        SocietyStore.changeLoading();
    };

    render() {
        return (
            <Form>
                <Form.Item>
                    <Search
                        value={SocietyStore.query}
                        onChange={this.handleQueryChange}
                        onSearch={this.handleSearch}
                        allowClear
                    />
                </Form.Item>
            </Form>
        )
    }
}

export default SocietySearch;