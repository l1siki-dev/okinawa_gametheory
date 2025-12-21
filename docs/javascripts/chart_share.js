/**
 * Final Viral Chart Script
 * 1. Generates Image
 * 2. Copies Text/URL to Clipboard (Fix for Android/Twitter)
 * 3. Opens Native Share
 */
async function shareChart(elementId) {
    var dom = document.getElementById(elementId);
    if (!dom) return;

    var chartInstance = echarts.getInstanceByDom(dom);
    if (!chartInstance) {
        alert("Chart not loaded yet.");
        return;
    }

    // 1. Get Image Data (High Res)
    var dataURL = chartInstance.getDataURL({
        type: 'png',
        pixelRatio: 2,
        backgroundColor: '#ffffff'
    });

    // 2. Prepare Data
    var blob = await (await fetch(dataURL)).blob();
    var file = new File([blob], "osint_analysis.png", { type: "image/png" });
    
    // The viral text with your URL
    var shareText = `Read more: ${window.location.href}`;

    // 3. ANDROID FIX: Copy text to clipboard silently first
    try {
        await navigator.clipboard.writeText(shareText);
        showToast("URL copied! Paste it in your post 📋");
    } catch (err) {
        console.log("Clipboard failed (non-HTTPS site?)");
    }

    // 4. Share
    if (navigator.canShare && navigator.canShare({ files: [file] })) {
        try {
            // We still send text for apps that DO support it (like Email/Telegram)
            await navigator.share({
                files: [file],
                title: 'OSINT Report',
                text: shareText 
            });
        } catch (error) {
            console.log("Share closed", error);
        }
    } else {
        // Desktop Fallback
        try {
            const item = new ClipboardItem({ 'image/png': blob });
            await navigator.clipboard.write([item]);
            alert("Image copied! \n(Caption is also in your clipboard)");
        } catch (err) {
            alert("Browser does not support sharing.");
        }
    }
}

// Helper: Shows a little popup notification (No CSS file needed)
function showToast(message) {
    var toast = document.createElement("div");
    toast.innerText = message;
    toast.style.position = "fixed";
    toast.style.top = "30%";
    toast.style.left = "50%";
    toast.style.transform = "translateX(-50%)";
    toast.style.backgroundColor = "rgba(0,0,0,0.8)";
    toast.style.color = "#fff";
    toast.style.padding = "10px 20px";
    toast.style.borderRadius = "20px";
    toast.style.zIndex = "9999";
    toast.style.fontSize = "20px";
    toast.style.transition = "opacity 0.5s";
    
    document.body.appendChild(toast);
    
    // Fade out after 3 seconds
    setTimeout(function() {
        toast.style.opacity = "0";
        setTimeout(function() { document.body.removeChild(toast); }, 500);
    }, 3000);
}

// -------------------------------------------------------------
// HELPER: Auto-Render Logic (Keep this from previous step)
// -------------------------------------------------------------
function renderOsintChart(id, option) {
    var run = function() {
        var dom = document.getElementById(id);
        if (dom && typeof echarts !== 'undefined') {
            if (echarts.getInstanceByDom(dom)) return; 
            var myChart = echarts.init(dom);
            // Default Padding for Share Button
            if (!option.grid) option.grid = { top: 60, right: 20, bottom: 20, left: 40, containLabel: true };
            myChart.setOption(option);
            window.addEventListener('resize', function() { myChart.resize(); });
        }
    };
    if (document.readyState === 'complete') run();
    else window.addEventListener('load', run);
}

async function copyPageUrl() {
    try {
        await navigator.clipboard.writeText(window.location.href);
        showToast("Page link copied! 🔗");
    } catch (err) {
        // Fallback for rare browsers
        prompt("Copy this link:", window.location.href);
    }
}
