const graphHolder = document.getElementById("graphs")
const benchmarkForm = document.getElementById("benchmark")
const jsonInput = document.getElementById("tests-json");

// Generates Graphs
// Constants
const width = 928;
const height = 500;
const marginTop = 20;
const marginRight = 30;
const marginBottom = 30;
const marginLeft = 40;
const accentColor = "#2ED186";

// Benchmark Graph
const benchmarkGraph = (dataSet, xName, yName, addition = 0) => {
    const x = d3.scalePoint()
        .domain(d3.range(0, d3.max(dataSet, d => d.num) + 1))  // Test numbers on x-axis
        .range([marginLeft, width - marginRight]);  // Full width of the chart

    const y = d3.scaleLinear()
        .domain([0, d3.max(dataSet, d => d.elapsed) + addition])
        .range([height - marginBottom, marginTop]);

// Declare the area generator.
    const area = d3.area()
        .x(d => x(d.num))  // X: Test number
        .y0(y(0))  // Y0: Start at y=0 (baseline)
        .y1(d => y(d.elapsed));  // Y1: Elapsed time for each test

// Create the SVG container.
    const svg = d3.create("svg")
        .attr("viewBox", [0, 0, width, height])
        .attr("class", "graph");

// Append a path for the area (under the axes).
    svg.append("path")
        .attr("fill", accentColor)  // Use your accent color for the area
        .attr("d", area(dataSet));  // Apply the area generator to the dataset

// Add the x-axis (Test Numbers) with white text and lines.
    svg.append("g")
        .attr("transform", `translate(0,${height - marginBottom})`)
        .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0))
        .call(g => g.selectAll("text").attr("fill", "white"))  // X-axis text white
        .call(g => g.selectAll("line").attr("stroke", "white"))  // X-axis ticks white
        .call(g => g.selectAll("path").attr("stroke", "white"))  // X-axis line white
        .call(g => g.append("text")
            .attr("x", width - 25)
            .attr("y", marginBottom)
            .attr("fill", "white")
            .attr("text-anchor", "end")
            .text(xName));

// Add the y-axis (Elapsed Time) with white text and lines.
    svg.append("g")
        .attr("transform", `translate(${marginLeft},0)`)
        .call(d3.axisLeft(y).ticks(height / 40))  // Adjust y-axis ticks based on height
        .call(g => g.select(".domain").remove())  // Remove y-axis domain line
        .call(g => g.selectAll(".tick line").clone()
            .attr("x2", width - marginLeft - marginRight)
            .attr("stroke-opacity", 0.1)
            .attr("stroke", "white"))  // Grid lines white
        .call(g => g.selectAll("text").attr("fill", "white"))  // Y-axis text white
        .call(g => g.append("text")
            .attr("x", -marginLeft)
            .attr("y", 10)
            .attr("fill", "white")
            .attr("text-anchor", "start")
            .text(yName));  // Label for y-axis

    return svg.node();
}

// Benchmark Graph
const rateGraph = (dataSet) => {
    // Data structure should have counts for successes and failures
    const data = [{category: 'Success', count: dataSet.filter(d => d.success).length}, {
        category: 'Failure',
        count: dataSet.filter(d => !d.success).length
    }];

    // Declare the x (horizontal position) scale.
    const x = d3.scaleBand()
        .domain(data.map(d => d.category)) // 'Success' and 'Failure'
        .range([marginLeft, width - marginRight])
        .padding(0.1);

    // Declare the y (vertical position) scale.
    const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.count)])  // Set max to the highest count
        .range([height - marginBottom, marginTop]);

    // Create the SVG container.
    const svg = d3.create("svg")
        .attr("viewBox", [0, 0, width, height])
        .attr("class", "graph");

    // Add a rect for each bar (Success and Failure).
    svg.append("g")
        .attr("fill", accentColor)  // Set your custom accent color for bars
        .selectAll("rect")
        .data(data)
        .join("rect")
        .attr("x", d => x(d.category))
        .attr("y", d => y(d.count))
        .attr("height", d => y(0) - y(d.count))
        .attr("width", x.bandwidth());

    // Add the x-axis with white text and lines.
    svg.append("g")
        .attr("transform", `translate(0,${height - marginBottom})`)
        .call(d3.axisBottom(x).tickSizeOuter(0))
        .call(g => g.selectAll("text").attr("fill", "white"))  // Make x-axis text white
        .call(g => g.selectAll("line").attr("stroke", "white"))  // Make x-axis tick lines white
        .call(g => g.selectAll("path").attr("stroke", "white"));  // Make x-axis line white

    // Add the y-axis with white text, lines, and grid lines.
    svg.append("g")
        .attr("transform", `translate(${marginLeft},0)`)
        .call(d3.axisLeft(y).ticks(5))
        .call(g => g.select(".domain").remove())  // Remove domain line
        .call(g => g.selectAll(".tick line").clone()
            .attr("x2", width - marginLeft - marginRight)
            .attr("stroke-opacity", 0.1)
            .attr("stroke", "white"))  // Grid lines white
        .call(g => g.selectAll("text").attr("fill", "white"))  // y-axis text white
        .call(g => g.append("text")
            .attr("x", -marginLeft)
            .attr("y", 10)
            .attr("fill", "white")
            .attr("text-anchor", "start")
            .text("Number of Tests"));  // y-axis label in white

    // Return the SVG element.
    return svg.node();
}

// Clears The Graphs
const clearGraphs = () => {
    while (graphHolder?.firstChild) {
        graphHolder.removeChild(graphHolder.firstChild);
    }
}

const loadJson = () => {
    fetch('/static/benchmark.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            return response.text();
        })
        .then(text => {
            jsonInput.value = text;
            JSON_TEST = text;
        })
        .catch(error => {
            alert("Could not load the default benchmark json file.")
        });
}

// Form Submit
let benchmarkBusy = false;
const globalBenchmarkDataSet = [];
const onBenchmarkSubmit = (event) => {
    event.preventDefault();

    if (benchmarkBusy || !benchmarkForm || !jsonInput) return;

    if (!benchmarkForm.checkValidity()) return;

    benchmarkBusy = true;

    benchmarkForm.setAttribute("data-loading", "true");
    jsonInput.disabled = true;

    const data = {};

    try {
        data.tests = JSON.parse(jsonInput.value)
    } catch (err) {
        alert("Invalid json syntax.");
        benchmarkForm.setAttribute("data-loading", "false");
        jsonInput.disabled = false;
        benchmarkBusy = false;
        return;
    }


    // Making the request
    fetch('/benchmark', {
        method: 'POST', // Specify the request method
        headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(({result, error, duration}) => {
            if (error) throw error;

            const dataSet = []

            result.forEach(({elapsed, success}, i) => {
                dataSet.push({
                    num: i,
                    success,
                    elapsed: elapsed * 1000,
                });
            })

            globalBenchmarkDataSet.push({elapsed: duration, num: globalBenchmarkDataSet.length})

            clearGraphs();

            // Current Benchmark
            const h_bench = document.createElement("h5");
            const p_bench = document.createElement("p");
            h_bench.innerHTML = "Current Benchmark Graph";
            p_bench.innerHTML = "Analyzes the performance of each individual test within the current benchmark tests."
            graphHolder.append(h_bench, p_bench, benchmarkGraph(dataSet, "Test Number", "Elapsed Time (ms)", 1));

            // Current Test
            const h_rate = document.createElement("h5");
            const p_rate = document.createElement("p");
            h_rate.innerHTML = "Current Success Rate Graph";
            p_rate.innerHTML = "Displays the number of individual tests within the current benchmark that have succeeded."
            graphHolder.append(h_rate, p_rate, rateGraph(dataSet));

            // Compare Test
            const h_comp = document.createElement("h5");
            const p_comp = document.createElement("p");
            h_comp.innerHTML = "Benchmark Comparison";
            p_comp.innerHTML = "Analyzes the comparison between benchmarks. This graph will update automatically as more benchmarks are conducted."
            graphHolder.append(h_comp, p_comp, benchmarkGraph(globalBenchmarkDataSet, "Benchmark Number", "Elapsed Time (sec)", 1 / 1000));
        })
        .catch(error => {
            alert("Oops something went wrong!");
            console.error(error);
        })
        .finally(() => {
            benchmarkForm.setAttribute("data-loading", "false");
            jsonInput.disabled = false;
            benchmarkBusy = false;
        });
}

// Init
benchmarkForm?.addEventListener("submit", onBenchmarkSubmit)
loadJson();

/* Cleaning */
window.addEventListener('beforeunload', function () {
    benchmarkForm?.removeEventListener('submit', onBenchmarkSubmit);
});