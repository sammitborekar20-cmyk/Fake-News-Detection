async function fetchSocialMediaData(platform) {
    let apiUrl = "";
    let headers = {};

    if (platform === "twitter") {
        apiUrl = "https://api.twitter.com/2/tweets/search/recent?query=india";
        headers = { "Authorization": "AAAAAAAAAAAAAAAAAAAAAPQg0QEAAAAAyZQVMF21k0a2T7Ng39ynYIB2Agg%3DHPgnKDZIRL8uQzvbu1G9G69DfCrI4lNEC5N6GU3uhcJjK9FNuk" };
    } else if (platform === "reddit") {
        apiUrl = "https://www.reddit.com/r/news/top.json";
        headers = { "User-Agent": "ChromeExtension/1.0" };
    } else if (platform === "facebook") {
        apiUrl = "https://graph.facebook.com/v17.0/me/feed?access_token=YOUR_FACEBOOK_ACCESS_TOKEN";
    }

    try {
        let response = await fetch(apiUrl, { method: "GET", headers });
        let data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching data:", error);
        return { error: "Failed to fetch data" };
    }
}

// Listen for messages from popup.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "fetch_data") {
        fetchSocialMediaData(request.platform).then(data => sendResponse({ success: true, data }))
            .catch(error => sendResponse({ success: false, error: error.message }));
        return true;
    }
});


