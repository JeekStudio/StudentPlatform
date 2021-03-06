import React from 'react';
import PropTypes from 'prop-types';
import {Tag} from 'antd';

const colorList = [
    "magenta",
    "red",
    "volcano",
    "orange",
    "gold",
    "lime",
    "green",
    "cyan",
    "blue",
    "geekblue",
    "purple"
];

class TagContainer extends React.Component {
    render() {
        const tag = this.props.tags;

        return (
            <div style={{display: 'none'}}>
                {tag.map((item, index) => {
                    return <Tag className="society-tag" key={index} color={colorList[Math.floor(Math.random() * colorList.length)]}>{item}</Tag>
                })}
            </div>
        )
    }
}

TagContainer.propTypes = {
    tags: PropTypes.array
};

export default TagContainer;