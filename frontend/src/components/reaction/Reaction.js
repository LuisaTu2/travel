import { useState, useEffect } from "react";

import "./Reaction.css";

import { UPDATE_PHOTO, DELETE_LIKE, mapping } from "../../constants.js";

export default function Reaction({reaction, isLast, ipAddress, pk, sk}) {
    // const mapping = {
    //     "doggo" :  "🐶",
    //     "sun" : "☀️",
    //     "heart": "❤",
    //     "blue_heart": "💙",
    //     "black_heart": "🖤",
    //     "grey_heart": "🩶",
    //     "yellow_heart": "💛",
    //     "purple_heart": "💜",
    //     "pink_heart": "🩷",
    //     "white_heart": "🤍",
    //     "light_blue_heart": "🩵",
    //     "green_heart": "💚",
    //     "orange_heart": "🧡",
    //     "serbia_flag": "🇷🇸",
    //     "flower": "🌺",
    //     "coffee": "☕",
    //     "eyes": "👀",
    //     "rose": "🌹",
    //     "swimming_pool": "🌊",
    //     "exclamation": "❗",
    //     "traffic_light": "🚦",
    //     "sparkle": "✨",
    //     "minibus": "🚐",
    //     "yellow": "🟡",
    //     "zap" : "⚡",
    //     "paintbrush": "🖌️",
    //     "dog": "🐶",
    //     "cat": "🐱",
    //     "black_cat" : "🐈‍⬛",
    //     "car": "🚗",
    //     "fish": "🐠",
    //     "feather": "🪶",
    //     "candle": "🕯️",
    //     "notes": "🎶",
    //     "trolleybus": "🚎",
    //     "fart": "💨"
    // }
    const emojiName = reaction[0]
    const emoji = mapping[reaction[0]];
    const initialLikes = reaction[1].likes;
    const ipAddresses = reaction[1].liked_by;
    const reactionIsLiked = ipAddresses.hasOwnProperty(ipAddress)  

    const [likes, setLikes] = useState(initialLikes);
    const [reactionStyle, setReactionStyle] = useState("reaction");
    useEffect(() => {
        if(reactionIsLiked){
            setReactionStyle("reactionLiked")
        }
    },[]);

    const addLike = async () => {
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
        setReactionStyle("reactionLiked")
        const updatedLikes = likes + 1;
        setLikes(updatedLikes)
        // const data = await response.json();
        // console.log("DATA: ", data)
    }

    const deleteLike = async () => {
        if (likes === 0){
            return
        }

        const response = await fetch(DELETE_LIKE, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }, 
            body: JSON.stringify({
                key: {pk, sk},
                reaction: emojiName,
                ipAddress: ipAddress
            })
        }); 
        const data = await response.json();
        console.log("RESPONSE: ", data)
        setReactionStyle("reaction")
        const updatedLikes = likes - 1;
        setLikes(updatedLikes)
    }

    const handleOnClick = event => {
        console.log("EVENT: ", event, ipAddress, ipAddresses, reactionIsLiked)
        if (reactionIsLiked) {
            deleteLike();
            return;
        }
        addLike();
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
