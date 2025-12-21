document.addEventListener("DOMContentLoaded", function() {
    // Select all headers you want to be shareable (e.g., h2 and h3)
    const headers = document.querySelectorAll("h2, h3");

    headers.forEach(header => {
        // Create the share button
        const shareBtn = document.createElement("button");
        shareBtn.innerHTML = "⌲"; // You can use an SVG icon here instead
        shareBtn.className = "header-share-btn";
        shareBtn.title = "Share this section";

        shareBtn.onclick = () => {
            const url = window.location.origin + window.location.pathname + "#" + header.id;
            const title = header.innerText.replace("⌲", "").trim();

            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(console.error);
            } else {
                // Fallback: Copy to clipboard if Web Share API isn't supported
                navigator.clipboard.writeText(url);
                alert("Link copied to clipboard!");
            }
        };

        header.appendChild(shareBtn);
    });
});
