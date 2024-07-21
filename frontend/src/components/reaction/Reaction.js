import { useState, useEffect } from "react";

import "./Reaction.css";

import { UPDATE_PHOTO } from "../../constants.js";

export default function Reaction({reaction, isLast, ipAddress, pk, sk}) {
    const mapping = {
        "doggo" :  "🐶",
        "sun" : "☀️",
        "heart": "❤",
        "blue_heart": "💙",
        "black_heart": "🖤",
        "grey_heart": "🩶",
        "yellow_heart": "💛",
        "purple_heart": "💜",
        "white_heart": "🤍",
        "flower": "🌺",
        "coffee": "☕",
        "eyes": "👀",
        "rose": "🌹",
        "swimming_pool": "🌊",
        "exclamation": "❗",
        "traffic_light": "🚦",
        "sparkle": "✨",
        "minibus": "🚐",
        "yellow": "🟡",
        "zap" : "⚡",
        "paintbrush": "🖌️",
        "dog": "🐶",
        "cat": "🐱",
        "black_cat" : "🐈‍⬛",
        "car": "🚗",
        "fish": "🐠",
        "feather": "🪶",
        "candle": "🕯️",
        "notes": "🎶",
        "trolleybus": "🚎",
        "fart": "💨"
    }
    const emojiName = reaction[0]
    const emoji = mapping[reaction[0]];
    const initialLikes = reaction[1].likes;
    const ipAddresses = reaction[1].liked_by;
    const reactionAlreadyLiked = ipAddresses.hasOwnProperty(ipAddress)  

    const [likes, setLikes] = useState(initialLikes);
    const [reactionStyle, setReactionStyle] = useState("reaction");
    useEffect(() => {
        if(reactionAlreadyLiked){
            setReactionStyle("reactionSeen")
        }
    },[]);

    const updateLikes = async () => {

        await fetch(UPDATE_PHOTO, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }, 
            body: JSON.stringify({
                key: {pk, sk},
                reaction: emojiName,
            })
        }); 
        setReactionStyle("reactionSeen")
        const updatedLikes = likes + 1;
        setLikes(updatedLikes)
        // const data = await response.json();
        // console.log("DATA: ", data)
    }

    const handleOnClick = event => {
        console.log("EVENT: ", event, ipAddress, ipAddresses, reactionAlreadyLiked)
        if (reactionAlreadyLiked) {
            return null;
        }
        updateLikes();
    }

    const element = (
        <div className="reactionBox" >
            <div className={reactionStyle}  >
                <p className="emoji" onClick={handleOnClick}> {emoji}  </p>
                <p className="likes"> {likes} </p>
            </div>
            {isLast ? "" : <p className="dot"> &#183; </p>}
        </div>
    );

        {/* <p className="photoReactions" onClick={event => { console.log("EVENT: ", event); event.target.style.color = "grey"}}>
    </p> */}
    return element;
}
