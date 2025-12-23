/**
 * Final Viral Chart Script
 * Includes Lazy Loading (Intersection Observer)
 * Updates: Auto-extracts metadata and formats text for viral sharing.
 */

// -------------------------------------------------------------
// PART 1: Share & Copy Logic
// -------------------------------------------------------------
async function shareChart(elementId) {
    var dom = document.getElementById(elementId);
    if (!dom) return;

    var chartInstance = echarts.getInstanceByDom(dom);
    if (!chartInstance) {
        alert("Chart is loading... please wait a moment."); 
        return;
    }

    // --- A. Generate Content ---

    // 1. Get Image Data
    var dataURL = chartInstance.getDataURL({
        type: 'png',
        pixelRatio: 2,
        backgroundColor: '#ffffff'
    });

    // 2. Prepare Blob & File
    var blob = await (await fetch(dataURL)).blob();
    var file = new File([blob], "osint_analysis.png", { type: "image/png" });

    // 3. Construct Viral Text
    
    // Get Metadata (Fallback to hardcoded if meta tags missing)
    const metaSiteName = document.querySelector('meta[property="og:site_name"]')?.content || "Okinawa is designed to fail";
    const metaAuthor = document.querySelector('meta[name="author"]')?.content || "りしき";

    // Get Chart Title (From ECharts options)
    // ECharts options usually store title in an array or object
    const chartOpts = chartInstance.getOption();
    let chartTitle = "Data Visualization";
    if (chartOpts.title && chartOpts.title.length > 0 && chartOpts.title[0].text) {
        chartTitle = chartOpts.title[0].text;
    }

    // specific URL to this chart
    const shareUrl = window.location.origin + window.location.pathname + "#" + elementId;

    // The Viral String
    const shareText = `"${chartTitle}"\nvia ${metaSiteName} (by ${metaAuthor})\n${shareUrl}`;

    // --- B. Execute Share ---

    // 4. Android Clipboard Fix (Copy text first)
    try {
        await navigator.clipboard.writeText(shareText);
        showToast("Caption copied! 📋");
    } catch (err) {
        console.log("Clipboard failed (non-HTTPS site?)");
    }

    // 5. Native Share (Mobile) or Fallback (Desktop)
    if (navigator.canShare && navigator.canShare({ files: [file] })) {
        try {
            await navigator.share({
                files: [file],
                title: chartTitle,
                text: shareText 
            });
        } catch (error) {
            console.log("Share closed", error);
        }
    } else {
        // Desktop / Browser without Web Share API support
        try {
            // Try to write the image to clipboard (Chrome/Edge supports this)
            const item = new ClipboardItem({ 'image/png': blob });
            await navigator.clipboard.write([item]);
            
            // Re-copy text to ensure it's available (Image + Text paste isn't always supported)
            // Note: Browsers usually only allow one item type at a time in clipboard.
            // We prioritize the Text for viral context, or Image for visual.
            // Strategy: Alert the user that text is in clipboard, image is in file.
            // Actually, let's copy text to clipboard and download image? 
            // Standard behavior: Copy text, user manually saves image or screenshots.
            // But here we try to copy image.
            
            alert(`Image copied to clipboard!\n\nThe caption has also been generated:\n${shareText}`);
        } catch (err) {
            alert("Browser limit: Right-click the chart to save image.\n\nCaption:\n" + shareText);
        }
    }
}

function showToast(message) {
    var toast = document.createElement("div");
    toast.innerText = message;
    toast.style.position = "fixed";
    toast.style.top = "20%"; // Slightly higher to not block chart
    toast.style.left = "50%";
    toast.style.transform = "translateX(-50%)";
    toast.style.backgroundColor = "rgba(0,0,0,0.85)"; // Slightly darker
    toast.style.color = "#fff";
    toast.style.padding = "12px 24px";
    toast.style.borderRadius = "30px";
    toast.style.zIndex = "9999";
    toast.style.fontSize = "16px";
    toast.style.fontWeight = "bold";
    toast.style.transition = "opacity 0.5s";
    toast.style.boxShadow = "0 4px 12px rgba(0,0,0,0.3)";
    
    document.body.appendChild(toast);
    setTimeout(function() {
        toast.style.opacity = "0";
        setTimeout(function() { document.body.removeChild(toast); }, 500);
    }, 3000);
}

// Function to copy URL with specific ID tag (Helper)
function copyPageUrl(id) {
    const url = window.location.origin + window.location.pathname + "#" + id;
    navigator.clipboard.writeText(url).then(() => {
        showToast("Deep-link copied!");
    });
}

// -------------------------------------------------------------
// PART 2: Lazy Load Logic (Kept mostly same, added safety checks)
// -------------------------------------------------------------

document.addEventListener("DOMContentLoaded", function () {
    const chartObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const dom = entry.target;
                const id = dom.id;
                
                const options = window.osintChartData ? window.osintChartData[id] : null;

                if (options && typeof echarts !== 'undefined') {
                    if (echarts.getInstanceByDom(dom)) return;

                    const myChart = echarts.init(dom);
                    
                    if (!options.grid) {
                        options.grid = { top: 60, right: 20, bottom: 20, left: 40, containLabel: true };
                    }

                    myChart.setOption(options);
                    window.addEventListener('resize', function() { myChart.resize(); });
                    
                    observer.unobserve(dom);
                }
            }
        });
    }, { 
        threshold: 0.1, // Lower threshold slightly to load sooner
        rootMargin: "50px" // Start loading before it hits viewport
    });

    const lazyCharts = document.querySelectorAll('.lazy-chart');
    lazyCharts.forEach(chart => {
        chartObserver.observe(chart);
    });
});
