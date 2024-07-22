import { useState, useEffect } from "react";

import "./Reaction.css";

import { UPDATE_PHOTO, DELETE_LIKE, mapping, HEADERS } from "../../constants.js";

export default function Reaction({reaction, isLast, ipAddress, pk, sk}) {

    const emojiName = reaction[0]
    const emoji = mapping[reaction[0]];
    const initialLikes = reaction[1].likes;
    const ipAddresses = reaction[1].liked_by;
    const reactionIsInitiallyLiked = ipAddresses.hasOwnProperty(ipAddress)  

    const [likes, setLikes] = useState(initialLikes);
    const [liked, setLiked] = useState(false);
    const [reactionStyle, setReactionStyle] = useState("reaction");
    useEffect(() => {
        if(reactionIsInitiallyLiked){
            setReactionStyle("reactionLiked");
            setLiked(true);
        }
    },[]);

    const addLike = async () => {
        await fetch(UPDATE_PHOTO, {
            method: 'POST',
            headers: HEADERS, 
            body: JSON.stringify({
                key: {pk, sk},
                reaction: emojiName,
            })
        }); 
        setReactionStyle("reactionLiked")
        setLikes(likes  + 1)
        setLiked(!liked)
    }

    const deleteLike = async () => {
        if (likes === 0){
            return
        }

        await fetch(DELETE_LIKE, {
            method: 'POST',
            headers: HEADERS, 
            body: JSON.stringify({
                key: {pk, sk},
                reaction: emojiName,
                ip_address: ipAddress
            })
        }); 
        setReactionStyle("reaction")
        setLikes(likes - 1)
        setLiked(!liked)
    }

    const handleOnClick = event => {
        if (liked) {
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

    return element;
}
