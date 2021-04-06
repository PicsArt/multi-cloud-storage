import React from 'react';

class HelloMessage extends React.Component {
    render() {
        return (
            <div>
                Hello {this.props.name}
            </div>
        );
    }
}
export default HelloMessage;

// ReactDOM.render(
//     <HelloMessage name="Taylor" />,
//     document.getElementById('hello-example')
// );