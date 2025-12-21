---
title: Succeeded at Failing
---
# Summary
© 2025 伊波りしき. This work is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

Based on selectorate theory, game theory, resource curse, aid curse, incentive analysis, and rational choice theory.

---

    

<script>
  // Standard ECharts setup
  var myChart = echarts.init(document.getElementById('my-graph-id'));
  var option = {
      // Don't forget: No 'toolbox' here anymore!
      grid: { top: 60, right: 30 }, // Add top padding so the button doesn't cover the highest bar
      xAxis: { type: 'category', data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'] },
      yAxis: { type: 'value' },
      series: [{ data: [820, 932, 901, 934, 1290], type: 'bar' }]
  };
  myChart.setOption(option);
</script>

---
# Bar Chart Example
<div style="position: relative; width: 100%; max-width: 800px;">
<div id="chart-container" style="width: 600px;height:400px;">
    <button class="md-button md-button--primary" 
        onclick="shareChart('chart-container')"
        style="position: absolute; top: 10px; right: 10px; z-index: 10; padding: 6px 12px; font-size: 0.8rem; line-height: 1.2; min-width: auto;">
    📤 Share
    </button>

</div>
</div>

<script>
  // Initialize the ECharts instance upon page load
  document.addEventListener('DOMContentLoaded', (event) => {
    var chartDom = document.getElementById('chart-container');
    var myChart = echarts.init(chartDom);
    var option;

    // Specify the configuration and data for the chart
    option = {
      title: {
        text: 'ECharts Bar Chart'
      },
      backgroundColor: '#ffffff', 
      graphic: [
        {
          type: 'text',
          right: 10,  // Position: Bottom Right
          bottom: 10,
          style: {
            text: '© MyOSINTReport.com | @MyHandle', // YOUR BRAND
            fill: '#888888', // Subtle Grey
            fontSize: 12,
            fontWeight: 'bold'
          }
        }
      ],
      tooltip: {},
      legend: {
        data: ['Sales']
      },
      xAxis: {
        data: ['Shirt', 'Cardigan', 'Chiffon Shirt', 'Pants', 'Heels', 'Pumps']
      },
      yAxis: {},
      series: [
        {
          name: 'Sales',
          type: 'bar',
          data: [5, 20, 36, 10, 10, 20]
        }
      ]
    };

    // Render the chart using the configuration
    myChart.setOption(option);
  });
</script>


<script>
async function shareChart() {
    // 1. Get the ECharts instance (Make sure ID matches your div)
    var chartInstance = echarts.getInstanceByDom(document.getElementById('chart-container'));

    if (!chartInstance) {
        alert("Chart not found!");
        return;
    }

    // 2. Convert Chart to a "Blob" (File object)
    var dataURL = chartInstance.getDataURL({
        type: 'png',
        pixelRatio: 2,        // High res for Retina/Twitter
        backgroundColor: '#fff' // FORCE White background
    });
    
    // Helper function to convert Base64 to Blob
    var blob = await (await fetch(dataURL)).blob();
    
    // 3. Create a File object
    var file = new File([blob], "osint-report.png", { type: "image/png" });

    // 4. Check if browser supports sharing files
    if (navigator.canShare && navigator.canShare({ files: [file] })) {
        try {
            await navigator.share({
                title: 'OSINT Report Data',
                text: 'Look at this spike 💀 detected in the latest dataset:', // The default tweet text
                files: [file]
            });
        } catch (error) {
            console.log('Sharing failed', error);
        }
    } else {
        // Fallback for browsers that don't support Web Share (mostly Desktop)
        alert("Your browser doesn't support direct image sharing. Using clipboard instead!");
        
        // Copy to clipboard fallback
        const item = new ClipboardItem({ 'image/png': blob });
        navigator.clipboard.write([item]);
        alert("Graph copied to clipboard! You can paste it into Twitter now.");
    }
}
</script>


---
## Key data
### Desicion-corrupting dependency (Okinawa 107.6%; National avg 11.5%)
Naha politicians' optimal financial strategy is vastly different from that of other prefectural governors.  
Naha has small (or negative to get more aid) incentives to take care of the local economy, or a healthy local society that produces tax revenue.  


![https://quickchart.io/sandbox/#%7B%22chart%22%3A%22%7B%5Cr%5Cn%20%20%5C%22type%5C%22%3A%20%5C%22bar%5C%22%2C%5Cr%5Cn%20%20%5C%22data%5C%22%3A%20%7B%5Cr%5Cn%20%20%20%20%5C%22labels%5C%22%3A%20%5B%5Cr%5Cn%5C%22Tokyo%20(3.1%25)%5C%22%2C%5C%22Kanagawa%20(3.2%25)%5C%22%2C%5C%22Osaka%20(4.2%25)%5C%22%2C%5C%22Aichi%20(4.4%25)%5C%22%2C%5C%22Saitama%20(4.5%25)%5C%22%2C%5C%22Shizuoka%20(6.5%25)%5C%22%2C%5C%22Ibaraki%20(6.9%25)%5C%22%2C%5C%22Hyogo%20(7.7%25)%5C%22%2C%5C%22Chiba%20(8.3%25)%5C%22%2C%5C%22Gunma%20(8.6%25)%5C%22%2C%5C%22Tochigi%20(8.9%25)%5C%22%2C%5C%22Shiga%20(8.9%25)%5C%22%2C%5C%22Kyoto%20(9.6%25)%5C%22%2C%5C%22Hiroshima%20(9.7%25)%5C%22%2C%5C%22Okayama%20(10.0%25)%5C%22%2C%5C%22Fukuoka%20(10.4%25)%5C%22%2C%5C%22Nagano%20(10.8%25)%5C%22%2C%5C%22Mie%20(11.2%25)%5C%22%2C%5C%22Nationwide%20(11.5%25)%5C%22%2C%5C%22Gifu%20(12.8%25)%5C%22%2C%5C%22Kagawa%20(13.5%25)%5C%22%2C%5C%22Ehime%20(14.4%25)%5C%22%2C%5C%22Ishikawa%20(15.2%25)%5C%22%2C%5C%22Nara%20(15.7%25)%5C%22%2C%5C%22Yamanashi%20(16.6%25)%5C%22%2C%5C%22Yamaguchi%20(17.4%25)%5C%22%2C%5C%22Toyama%20(17.6%25)%5C%22%2C%5C%22Fukui%20(18.6%25)%5C%22%2C%5C%22Tokushima%20(19.4%25)%5C%22%2C%5C%22Miyagi%20(20.3%25)%5C%22%2C%5C%22Niigata%20(21.4%25)%5C%22%2C%5C%22Aomori%20(22.4%25)%5C%22%2C%5C%22Saga%20(23.4%25)%5C%22%2C%5C%22Wakayama%20(23.8%25)%5C%22%2C%5C%22Yamagata%20(24.4%25)%5C%22%2C%5C%22Oita%20(24.6%25)%5C%22%2C%5C%22Hokkaido%20(25.6%25)%5C%22%2C%5C%22Kochi%20(27.2%25)%5C%22%2C%5C%22Tottori%20(31.7%25)%5C%22%2C%5C%22Shimane%20(31.8%25)%5C%22%2C%5C%22Akita%20(34.3%25)%5C%22%2C%5C%22Iwate%20(35.6%25)%5C%22%2C%5C%22Miyazaki%20(37.5%25)%5C%22%2C%5C%22Nagasaki%20(37.9%25)%5C%22%2C%5C%22Kagoshima%20(38.7%25)%5C%22%2C%5C%22Kumamoto%20(41.1%25)%5C%22%2C%5C%22Okinawa%20(107.6%25)%5C%22%20%20%20%20%5D%2C%5Cr%5Cn%20%20%20%20%5C%22datasets%5C%22%3A%20%5B%7B%5Cr%5Cn%20%20%20%20%20%20%5C%22label%5C%22%3A%20%5C%22Development%20Aid%2F%20Local%20Tax%20ratio%20(%25)%5C%22%2C%5Cr%5Cn%20%20%20%20%20%20%5C%22data%5C%22%3A%20%5B%5Cr%5Cn%20%20%20%20%20%20%20%203.1%2C%203.2%2C%204.2%2C%204.4%2C%204.5%2C%206.5%2C%206.9%2C%207.7%2C%208.3%2C%208.6%2C%208.9%2C%208.9%2C%209.6%2C%209.7%2C%2010.0%2C%20%5Cr%5Cn%20%20%20%20%20%20%20%2010.4%2C%2010.8%2C%2011.2%2C%2011.5%2C%2012.8%2C%2013.5%2C%2014.4%2C%2015.2%2C%2015.7%2C%2016.6%2C%2017.4%2C%2017.6%2C%2018.6%2C%20%5Cr%5Cn%20%20%20%20%20%20%20%2019.4%2C%2020.3%2C%2021.4%2C%2022.4%2C%2023.4%2C%2023.8%2C%2024.4%2C%2024.6%2C%2025.6%2C%2027.2%2C%2031.7%2C%2031.8%2C%2034.3%2C%20%5Cr%5Cn%20%20%20%20%20%20%20%2035.6%2C%2037.5%2C%2037.9%2C%2038.7%2C%2041.1%2C%20107.6%5Cr%5Cn%20%20%20%20%20%20%5D%2C%5Cr%5Cn%20%20%20%20%20%20%5C%22backgroundColor%5C%22%3A%20%5C%22rgba(54%2C%20162%2C%20235%2C%200.5)%5C%22%2C%5Cr%5Cn%20%20%20%20%20%20%5C%22borderColor%5C%22%3A%20%5C%22rgba(54%2C%20162%2C%20235%2C%201)%5C%22%2C%5Cr%5Cn%20%20%20%20%20%20%5C%22borderWidth%5C%22%3A%201%5Cr%5Cn%20%20%20%20%7D%5D%5Cr%5Cn%20%20%7D%2C%5Cr%5Cn%20%20%5C%22options%5C%22%3A%20%7B%5Cr%5Cn%20%20%20%20%5C%22title%5C%22%3A%20%7B%5Cr%5Cn%20%20%20%20%20%20%5C%22display%5C%22%3A%20true%2C%5Cr%5Cn%20%20%20%20%20%20%5C%22text%5C%22%3A%20%5C%22Desicion-currupting%20dependency%20(Okinawa%20108%25%3B%20National%20avg%2012%25)%20latest%20from%20e-Stat%5C%5Cn%20lisiki-jp.github.io%2Fokinawa_gametheory%5C%22%5Cr%5Cn%20%20%20%20%7D%2C%5Cr%5Cn%20%20%20%20%5C%22scales%5C%22%3A%20%7B%5Cr%5Cn%20%20%20%20%20%20%5C%22xAxes%5C%22%3A%20%5B%7B%5Cr%5Cn%20%20%20%20%20%20%20%20%5C%22ticks%5C%22%3A%20%7B%5Cr%5Cn%20%20%20%20%20%20%20%20%20%20%5C%22autoSkip%5C%22%3A%20false%2C%5Cr%5Cn%20%20%20%20%20%20%20%20%20%20%5C%22minRotation%5C%22%3A%2090%5Cr%5Cn%20%20%20%20%20%20%20%20%7D%5Cr%5Cn%20%20%20%20%20%20%7D%5D%5Cr%5Cn%20%20%20%20%7D%5Cr%5Cn%20%20%7D%5Cr%5Cn%7D%5Cr%5Cn%22%2C%22width%22%3A900%2C%22height%22%3A500%2C%22version%22%3A%222%22%2C%22backgroundColor%22%3A%22%23fff%22%7D](https://quickchart.io/chart/render/zf-fb5a79cc-38d2-45b9-9192-2683f6a71fc9)


(Fukushima, 95%, is omitted because of the meltdown recovery.)  
(Data Source: e-Stat. FY2017 Settlement: the latest available on e-stat) https://www.e-stat.go.jp/dbview?sid=0003173301  
(Development aid = Natl. Treasury for Construction + Others; 国庫支出金:普通建設事業費支出金 + 国庫支出金:その他)  
[Explanation and full data here](#okinawa-is-the-permanent-disaster-zone-financially)    

---
### Malfunctioning Tourism: Profit comparison

Okinawa has been trying the 'Tourism Strategy' since the Ocean Expo in 1975. That is 50 Years.
If a core business strategy hasn't turned into a profit in 50 years, yet you refuse to change course and demand more money to double down... that is not a 'Plan.' It is a Religion.  
The Okinawa government claims that "Tourism is bigger than military rent," but the reality is that tourism only generates a fraction of the profit compared to military rent.

![https://quickchart.io/sandbox/#%7B%22chart%22%3A%22%7B%5Cr%5Cn%20%20%5C%22type%5C%22%3A%20%5C%22outlabeledPie%5C%22%2C%5Cr%5Cn%20%20%5C%22data%5C%22%3A%20%7B%5Cr%5Cn%20%20%20%20%5C%22labels%5C%22%3A%20%5B%5C%22Fiscal%20Aid%20(Subsidies)%2063.0%25%5C%22%2C%5C%22Other%20(Social%20Security)%2023.7%25%5C%22%2C%5C%22Military%20(Rent)%2011.2%25%5C%22%2C%5C%22Tourism%20(Business%20Profit)%201.9%25%5C%22%2C%5C%22Petroleum%200.2%25%5C%22%5D%2C%5Cr%5Cn%20%20%20%20%5C%22datasets%5C%22%3A%20%5B%7B%5Cr%5Cn%20%20%20%20%20%20%20%20%5C%22backgroundColor%5C%22%3A%20%5B%5C%22%23FF3784%5C%22%2C%20%5C%22%2336A2EB%5C%22%2C%20%5C%22%234BC0C0%5C%22%2C%20%5C%22%23F77825%5C%22%2C%20%5C%22%239966FF%5C%22%5D%2C%5Cr%5Cn%20%20%20%20%20%20%20%20%5C%22data%5C%22%3A%20%5B63.00%2C23.70%2C11.20%2C1.90%2C0.20%5D%5Cr%5Cn%20%20%20%20%7D%5D%5Cr%5Cn%20%20%7D%2C%5Cr%5Cn%20%20%5C%22options%5C%22%3A%20%7B%5Cr%5Cn%20%20%20%20%5C%22title%5C%22%3A%20%7B%5Cr%5Cn%20%20%20%20%20%20%5C%22display%5C%22%3A%20true%2C%5Cr%5Cn%20%20%20%20%20%20%5C%22text%5C%22%3A%20%5C%22OKINAWA%20INDUSTRY%20PROFIT%20COMPARISON%5C%5Cnlisiki-jp.github.io%2Fokinawa_gametheory%5C%22%5Cr%5Cn%20%20%20%20%7D%2C%5Cr%5Cn%20%20%20%20%5C%22plugins%5C%22%3A%20%7B%5Cr%5Cn%20%20%20%20%20%20%5C%22legend%5C%22%3A%20false%2C%5Cr%5Cn%5Cr%5Cn%20%20%20%20%20%20%5C%22outlabels%5C%22%3A%20%7B%5Cr%5Cn%20%20%20%20%20%20%20%20%5C%22text%5C%22%3A%20%5C%22%25l%5C%22%2C%5Cr%5Cn%20%20%20%20%20%20%20%20%5C%22color%5C%22%3A%20%5C%22white%5C%22%2C%5Cr%5Cn%20%20%20%20%20%20%20%20%5C%22stretch%5C%22%3A%202%2C%5Cr%5Cn%20%20%20%20%20%20%20%20%5C%22font%5C%22%3A%20%7B%5Cr%5Cn%20%20%20%20%20%20%20%20%20%20%5C%22resizable%5C%22%3A%20true%2C%5Cr%5Cn%20%20%20%20%20%20%20%20%20%20%5C%22minSize%5C%22%3A%2012%2C%5Cr%5Cn%20%20%20%20%20%20%20%20%20%20%5C%22maxSize%5C%22%3A%2018%5Cr%5Cn%20%20%20%20%20%20%20%20%7D%5Cr%5Cn%20%20%20%20%20%20%7D%5Cr%5Cn%20%20%20%20%7D%5Cr%5Cn%20%20%7D%5Cr%5Cn%7D%22%2C%22width%22%3A500%2C%22height%22%3A300%2C%22version%22%3A%222%22%2C%22backgroundColor%22%3A%22%23fff%22%7D](https://quickchart.io/chart/render/zf-4a2c9bfa-107c-44f0-affe-1b9934c9fb37)

Based on "第5次沖縄県観光振興基本計画改定版" and e-Stat.  
The terminology here is following the document from Okinawa govt.  
[Explanation and full data here](#the-profit-vs-the-revenue-stasstical-deception-to-mix-different-figures)    

---
### Okinawa local newspaper's political narrative market share: 99.43%

They read the local papers not for information, but for validation. They need daily confirmation that they are the protagonists of a tragedy, not the recipients of a subsidy.
The 99.4% share is the measure of how desperate that psychological need is.

![https://quickchart.io/chart-maker/edit/zm-7143138a-5399-4cad-b4b4-fdf2f48dda4a](https://quickchart.io/chart/render/zm-7143138a-5399-4cad-b4b4-fdf2f48dda4a)

Nikkei was excluded because of a narrative comparison on politics. Also, Nikkei is a partner of Shimpo (the other four never held that position); it has been proven by local papers that Nikkei is not a competitor for local papers.  
*   **Okinawa Local Papers**: Okinawa Times (124,255) + Ryukyu Shimpo(123,638) = **247,893** copies.  
*   **National Papers (without Nikkei)**: Yomiuri(453) + Asahi(620) + Mainichi(189) + Sankei(156) = **1,418** copies.  
[Explanation and full data here](#estimation-of-okinawa-local-newspaper-market-share-9943)

---
### Actions and statements are not aligned
The three players in the Henoko project show behavior not aligned with their stated intention.  
We have to know the real intent of these three.


| Player                 | Stated Goal (What they SAY)           | Current Strategy (What they DO)                       | SAY and DO align? | Current Goal (What they WANT; estimated from observing)                                        | 
| :--------------------- | :------------------------------------ | :---------------------------------------------------- | :---------------- | :--------------------------------------------------------------------------------------------- | 
| **US Regime**          | Ensure regional stability             | Apply consistent pressure to Japan                    | **YES**           | **Status Quo** (Functional base & geopolitical "tripwire", keep Japan dependent on US)         | 
| **Japan Regime**       | Resolve the "Futenma danger"          | Contain the issue to not spread into the majority Japanese voters; run an impossibly slow project     | **NO**            | **Status Quo** (Alliance managed, secure political position, keep Okinawa dependent on Tokyo)  | 
| **Okinawa Regime**     | Stop the base                         | Appeal to anti-base voters without effective action   | **NO**            | **Status Quo** (Maintain secure political position)                                            | 
| **Okinawa Newspapers** | Reflect the public will               | Focus on ineffective narratives; localize the problem | **NO**            | **Status Quo** (Protect monopoly market)                                                       | 
| **Japan Newspapers**   | Inform the public objectively         | Provide periodic, low-key coverage                    | **Partially**     | **Status Quo** (Safest, low-cost option)                                                       | 
| **Japanese Citizens**  | (No single consensus)                 | Remain largely passive and disengaged                 | **N/A**           | **N/A**                                                                                        | 
| **Okinawa Citizens**   | Stop the base                         | Engage in localized, direct protest                   | **YES**           | **Solve** (Stop the base)                                                                      | 























