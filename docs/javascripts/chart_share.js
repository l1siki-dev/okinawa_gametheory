async function shareChart(elementId) {
    var dom = document.getElementById(elementId);
    if (!dom) return;

    var chartInstance = echarts.getInstanceByDom(dom);
    if (!chartInstance) {
        alert("Chart not initialized!");
        return;
    }

    // 1. Get Image Data
    var dataURL = chartInstance.getDataURL({
        type: 'png',
        pixelRatio: 2,
        backgroundColor: '#ffffff'
    });

    // 2. Prepare the File
    var blob = await (await fetch(dataURL)).blob();
    var file = new File([blob], "osint_graph.png", { type: "image/png" });

    // 3. Prepare the Text + URL
    // We combine them because some apps ignore the 'url' param when an image is attached.
    var shareTitle = document.title || 'OSINT Report';
    var shareText = `Check out this data 💀 detected in the latest report.\n\nRead more: ${window.location.href}`;

    // 4. Share
    if (navigator.canShare && navigator.canShare({ files: [file] })) {
        try {
            await navigator.share({
                title: shareTitle,
                text: shareText,      // URL is baked into the text here
                files: [file]
            });
        } catch (err) {
            console.log("Share canceled", err);
        }
    } else {
        // Fallback for Desktop (Clipboard)
        try {
            const item = new ClipboardItem({ 'image/png': blob });
            await navigator.clipboard.write([item]);
            // Since we can't copy text AND image to clipboard at the same time easily,
            // we alert the user.
            alert("Image copied to clipboard! \n(Don't forget to paste the link manually)");
        } catch (err) {
            alert("Browser does not support sharing.");
        }
    }
}
