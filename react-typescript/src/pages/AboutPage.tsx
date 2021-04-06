import React from "react";
import {useHistory} from 'react-router-dom'

const AboutPage: React.FC = () => {
    const history = useHistory()
    return <>
        <h1>About Todos App</h1>
        <p>
            You stupid dirty animal
        </p>
        <button className='btn' onClick={() => history.push('/')}>Back to Todos</button>
    </>;
}

export default AboutPage
