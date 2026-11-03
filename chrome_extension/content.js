document.addEventListener("DOMContentLoaded", function () {
    let posts = [];

    //  Selectors for different social media platforms
    let twitterPosts = document.querySelectorAll("article div[lang]"); // Twitter
    let facebookPosts = document.querySelectorAll("div[role='article'] p"); // Facebook
    let redditPosts = document.querySelectorAll(".Post div[data-test-id='post-content']"); // Reddit

    //  Extract text from posts
    twitterPosts.forEach(post => posts.push(post.innerText));
    facebookPosts.forEach(post => posts.push(post.innerText));
    redditPosts.forEach(post => posts.push(post.innerText));

    let textContent = posts.join(" ");

    if (textContent.length > 100) { // Only check if enough text exists
        fetch("http://127.0.0.1:8000/predict/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: textContent })
        })
        .then(response => response.json())
        .then(data => {
            console.log("API Response:", data); // Debugging line

            //  Store prediction result in Chrome's local storage
            chrome.storage.local.set({ prediction: data.prediction }, function () {
                console.log("Prediction saved:", data.prediction);
            });

            //  Highlight fake news
            if (data.prediction === "Fake News") {
                twitterPosts.forEach(p => p.style.backgroundColor = "red");
                facebookPosts.forEach(p => p.style.backgroundColor = "red");
                redditPosts.forEach(p => p.style.backgroundColor = "red");
            }
        })
        .catch(error => console.error("Error:", error));
    }
});


