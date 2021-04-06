import React, {useState, useRef} from 'react'
import {render} from "react-dom";

interface TodoFormProps{
    onAdd(title: string): void
}
const TodoForm: React.FC<TodoFormProps> = (props) => {
    // const [title, setTitle] = useState<string>('')
    // const changeHandler = (event: React.ChangeEvent<HTMLInputElement>) => {
    //     setTitle(event.target.value)
    // }
    const ref = useRef<HTMLInputElement>(null)
    const keyPressHandler = (event: React.KeyboardEvent<HTMLInputElement>) => {
        if (event.key === 'Enter'){
            // console.log(ref.current!.value)
            props.onAdd(ref.current!.value)
            ref.current!.value = ""
        }
    }
    return (
        <div className="input-field mt2">
            <input
                // onChange={changeHandler}
                onKeyPress={keyPressHandler}
                // value={title}
                ref={ref}
                type="text"
                id="title"
                placeholder="Insert your task name"/>
            <label htmlFor="title" className="active" >
                input task body
            </label>

        </div>
    );

}

export default TodoForm
