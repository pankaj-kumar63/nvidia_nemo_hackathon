import React from 'react';
import YouTube from 'react-youtube';
import './VideoCarousel.css'
const VideoCarousel = ({ videoUrls }) => {
    console.log(videoUrls);

    // YouTube player options
    const opts = {
        height: '200',
        width: '300',
        playerVars: {
            autoplay: 0, // Enable autoplay
        },
    };

    // Function to extract video ID
    function extractVideoId(url) {
        const regex = /v=([a-zA-Z0-9_-]{11})/;
        const match = url.match(regex);
        return match ? match[1] : null;
    }

    // Extract video IDs from the list
    const videoIds = videoUrls.map(extractVideoId);
    console.log("Ids:", videoIds);

    return (
        <div className = "video-caraousel-body">
            { videoIds.length > 0 && videoIds.map((id, index) => (
                <YouTube key={index} videoId={id} opts={opts} />
            ))}
        </div>
    );
};

export default VideoCarousel;
