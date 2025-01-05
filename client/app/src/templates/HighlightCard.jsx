import React from 'react'
import "./css/highlightcards.css";
const HighlightCard = (props) => {
  return (
    <div id='hmain'>
      <h2 id='titl'>
        {props.title}
      </h2>
      <div id='details'>
        <div id='imgcontainer' >
        <img src='../src/assets/netprofit.png' /></div>
        <div>
            <p>
                {props.value}
            </p>
        </div>

      </div>
    </div>
  )
}

export default HighlightCard
