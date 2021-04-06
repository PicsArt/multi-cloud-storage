import React from 'react'
import {ITodo} from "../interfaces";
import CanvasJSReact from '../canvasjs.react';
var CanvasJSChart = CanvasJSReact.CanvasJSChart;


type TodoListProps = {
    todos: ITodo[]
    onToggle(id:number): void
    onRemove: (id:number) => void

}

const TodoList: React.FC<TodoListProps> = ({
    todos,
    onToggle,
    onRemove
}) =>{

    if (todos.length === 0){
        return <p className="center">Nothing todo yet</p>
    }

    const removeHandler = (event: React.MouseEvent, id:number) =>{
        event.preventDefault()
        onRemove(id)
    }
    var dataPoin = todos.reduce((r:{[index: string]:any}, c) => {
            var status: string = c.completed ? "Completed" : "InProgress"
            if (!r.hasOwnProperty(status)) {
                r[status] = 0;
            }
            r[status]++;
            return r
        }
        , {})

    var dataPoints = []

    for( const key in dataPoin){
        dataPoints.push({y: (dataPoin[key]/todos.length)*100, label: key})
    }


    console.log(dataPoints)
    const options = {
        exportEnabled: true,
        animationEnabled: true,
        title: {
            text: "Work Progress"
        },
        data: [{
            type: "pie",
            startAngle: 75,
            toolTipContent: "<b>{label}</b>: {y}%",
            showInLegend: "true",
            legendText: "{label}",
            indexLabelFontSize: 16,
            indexLabel: "{label} - {y}%",

            dataPoints: dataPoints
        }]
    }

    return (
        <>
            <ul>
                {
                    todos.map(todo => {
                        const classes = ['todo']
                        if (todo.completed){
                            classes.push('completed')
                        }
                        return (<li  className={classes.join(' ')} key={todo.id }>
                            <label>
                                <input type="checkbox" checked={todo.completed} onClick={onToggle.bind(null, todo.id)}/>
                                <span>{todo.title }</span>
                                <i className="material-icons red-text" onClick={(event) => removeHandler(event, todo.id)}>delete</i>
                            </label>
                        </li>);}
                    )
                }

            </ul>
            <CanvasJSChart options = {options}
                /* onRef={ref => this.chart = ref} */
            />

        </>

    );
}

export default TodoList