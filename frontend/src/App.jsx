import React, { useEffect, useState } from 'react';
import {
    SciChartSurface,
    NumericAxis,
    FastLineRenderableSeries,
    XyDataSeries,
    SciChartJsNavyTheme,
    HorizontalLineAnnotation,
    EHorizontalAnchorPoint,
    EVerticalAnchorPoint,
    SweepAnimation,
    MouseWheelZoomModifier,
    ZoomPanModifier,
    EXyDirection,
} from "scichart";

// Configure SciChart to load WebAssembly files from the public folder
SciChartSurface.configure({
    wasmUrl: "/scichart2d.wasm", // Path to the wasm file
    dataUrl: "/scichart2d.data", // Path to the data file
});

// Helper function to generate a unique ID for the chart root element
const generateGuid = () => {
    return 'chart-root-' + Math.random().toString(36).substring(2, 15);
};

// Function to create the chart
const createChart = async (divElementId) => {
    const { sciChartSurface, wasmContext } = await SciChartSurface.create(divElementId, {
        theme: new SciChartJsNavyTheme(),
    });

    // Add X and Y axes
    const xAxis = new NumericAxis(wasmContext, {
        axisTitle: "Time (s)",
        drawMajorGridLines: true,
        drawMinorGridLines: true,
    });
    const yAxis = new NumericAxis(wasmContext, {
        axisTitle: "Voltage (V)",
        drawMajorGridLines: true,
        drawMinorGridLines: true,
        visibleRange: { min: -10, max: 10 }, // Adjust based on your data range
    });
    sciChartSurface.xAxes.add(xAxis);
    sciChartSurface.yAxes.add(yAxis);

    // Fetch data from the API
    try {
        const response = await fetch("http://localhost:5000/files/1/channels");
        const data_ = await response.json();
        const { samplingRate, data: channel1 } = data_["channels"][0];

        // Calculate time values
        let xValues = channel1.map((_, index) => index / samplingRate);
        let yValues = channel1;

        // Fallback to static data if fetched data is invalid or empty
        if (!channel1 || channel1.length === 0) {
            console.warn("Fetched data is empty. Using static data.");
            xValues = [0, 1, 2, 3, 4];
            yValues = [1, -1, 2, -2, 0];
        }

        // Log the data for debugging
        console.log("Fetched Data:", data_);
        console.log("xValues:", xValues);
        console.log("yValues:", yValues);

        // Add a line series for the data
        const lineSeries = new FastLineRenderableSeries(wasmContext, {
            stroke: "steelblue",
            strokeThickness: 2,
        });
        lineSeries.dataSeries = new XyDataSeries(wasmContext, {
            xValues,
            yValues,
        });
        lineSeries.animation = new SweepAnimation({
            duration: 300,
            fadeEffect: true
        });
        sciChartSurface.renderableSeries.add(lineSeries);

        // Add chart modifiers for zooming and panning
        sciChartSurface.chartModifiers.add(
            new MouseWheelZoomModifier({
                growFactor: 0.001
            }),
            new ZoomPanModifier({
                xyDirection: EXyDirection.XYDirection,
                horizontalGrowFactor: 0.005,
                verticalGrowFactor: 0.005,
            })
        );

        // Add a horizontal line annotation at y = 0
        const zeroLine = new HorizontalLineAnnotation({
            y1: 0, // Position of the line
            stroke: "red", // Color of the line
            strokeThickness: 2, // Thickness of the line
            strokeDashArray: [5, 5], // Optional: Make the line dashed
            labelPlacement: {
                horizontalAnchorPoint: EHorizontalAnchorPoint.Left,
                verticalAnchorPoint: EVerticalAnchorPoint.Top,
            },
            axisLabelFill: "red", // Color of the label
            axisLabelStroke: "transparent",
            axisLabelStrokeThickness: 0,
            axisLabelPadding: 5,
        });
        sciChartSurface.annotations.add(zeroLine);
    } catch (error) {
        console.error('Error fetching or processing data:', error);
    }

    return { sciChartSurface };
};

// React component
function SciChart({ initChart, className, style }) {
    const [rootElementId] = useState(generateGuid()); // Generate a unique ID for the chart root element

    useEffect(() => {
        let sciChartSurface;

        const initializeChart = async () => {
            const { sciChartSurface: surface } = await initChart(rootElementId);
            sciChartSurface = surface; // Save the surface instance
        };

        initializeChart();

        // Cleanup function to delete the SciChartSurface when the component unmounts
        return () => {
            if (sciChartSurface) {
                sciChartSurface.delete();
            }
        };
    }, [initChart, rootElementId]);

    return <div id={rootElementId} className={className} style={style} />;
}

// Main App component
function App() {
    return (
        <div>
            <header>
                <h1>Brain Activity Visualization</h1>
            </header>
            <SciChart
                initChart={createChart}
                style={{ width: '100%', height: '500px' }}
            />
        </div>
    );
}

export default App;