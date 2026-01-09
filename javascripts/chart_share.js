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

    // 1. Get Image
    var dataURL = chartInstance.getDataURL({
        type: 'png',
        pixelRatio: 2,
        backgroundColor: '#ffffff'
    });
    var blob = await (await fetch(dataURL)).blob();
    var file = new File([blob], "osint_chart.png", { type: "image/png" });

    // 2. Prepare Viral Text
    const metaSiteName = document.querySelector('meta[property="og:site_name"]')?.content || "Okinawa is designed to fail";
    const metaAuthor = document.querySelector('meta[name="author"]')?.content || "りしき";
    
    // Get Chart Title
    const chartOpts = chartInstance.getOption();
    let chartTitle = "Data Analysis";
    if (chartOpts.title && chartOpts.title.length > 0 && chartOpts.title[0].text) {
        chartTitle = chartOpts.title[0].text;
    }

    const shareUrl = window.location.origin + window.location.pathname + "#" + elementId;
    const fullShareText = `"${chartTitle}"\nvia ${metaSiteName} (by ${metaAuthor})\n${shareUrl}`;

    // 3. THE FIX: Copy Text to Clipboard FIRST (The "Safety Net")
    try {
        await navigator.clipboard.writeText(fullShareText);
        // Show instruction clearly
        showToast("Text copied! Paste it after selecting the app. 📋");
    } catch (err) {
        console.log("Clipboard write failed");
    }

    // 4. Trigger Native Share
    if (navigator.canShare && navigator.canShare({ files: [file] })) {
        try {
            await navigator.share({
                files: [file],
                // We still try to pass title/text, but if the app ignores it,
                // the user has it in their clipboard from step 3.
                title: chartTitle,
                text: fullShareText 
            });
        } catch (error) {
            console.log("Share cancelled or failed", error);
        }
    } else {
        // Desktop fallback
        try {
            const item = new ClipboardItem({ 'image/png': blob });
            await navigator.clipboard.write([item]);
            alert("Image copied!\n\nThe caption text is also in your clipboard.\nPaste (Ctrl+V) to share.");
        } catch (err) {
            alert("Please right-click the chart to save it.\n\nCaption:\n" + fullShareText);
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
