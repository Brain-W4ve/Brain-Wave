import React, { useEffect, useState } from "react";
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
    BoxAnnotation,
    ECoordinateMode,
} from "scichart";

SciChartSurface.configure({
  wasmUrl: "/scichart2d.wasm",
  dataUrl: "/scichart2d.data",
});

const generateGuid = () => 'chart-root-' + Math.random().toString(36).substring(2, 15);

const createChart = async (divElementId, data) => {
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
        visibleRange: { min: -10, max: 10 }, // Adjust this range as needed
    });
    sciChartSurface.xAxes.add(xAxis);
    sciChartSurface.yAxes.add(yAxis);

    // Extract data
    const { samplingRate, attacks, data: channel1 } = data.channels[0];

    // Calculate time values (x-axis) and y-axis values
    const xValues = channel1.map((_, index) => index / samplingRate);
    const yValues = channel1;

    // Add a line series for the data
    const lineSeries = new FastLineRenderableSeries(wasmContext, {
        stroke: "steelblue",
        strokeThickness: 2,
    });
    lineSeries.dataSeries = new XyDataSeries(wasmContext, { xValues, yValues });
    lineSeries.animation = new SweepAnimation({ duration: 300, fadeEffect: true });
    sciChartSurface.renderableSeries.add(lineSeries);

    // Add chart modifiers for zooming and panning
    sciChartSurface.chartModifiers.add(
        new MouseWheelZoomModifier({ growFactor: 0.001 }),
        new ZoomPanModifier({ xyDirection: EXyDirection.XYDirection })
    );

    // Add a horizontal line annotation at y = 0
    const zeroLine = new HorizontalLineAnnotation({
        y1: 0,
        stroke: "red",
        strokeThickness: 2,
        strokeDashArray: [5, 5],
        labelPlacement: {
        horizontalAnchorPoint: EHorizontalAnchorPoint.Left,
        verticalAnchorPoint: EHorizontalAnchorPoint.Top,
        },
    });
    sciChartSurface.annotations.add(zeroLine);

    // Add attack annotations (box annotations for each attack)
    console.log(attacks);
    if (attacks) {
        attacks.forEach((attack) => {
        const startIndex = Math.max(0, Math.floor(attack.start * samplingRate));
        const endIndex = Math.min(yValues.length - 1, Math.ceil(attack.finish * samplingRate));

        const yValuesInRange = yValues.slice(startIndex, endIndex + 1);
        const minY = Math.min(...yValuesInRange);
        const maxY = Math.max(...yValuesInRange);

        const attackAnnotation = new BoxAnnotation({
            x1: attack.start,
            x2: attack.finish,
            y1: minY,
            y2: maxY,
            fill: "rgba(255, 0, 0, 0.4)",
            stroke: "red",
            strokeThickness: 1,
            toolTipText: `${attack.name}: Peak-to-peak = ${(maxY - minY).toFixed(2)}`,
        });

        sciChartSurface.annotations.add(attackAnnotation);
        });
}

return { sciChartSurface };
};

function SciChart({ data }) {
  const [rootElementId] = useState(generateGuid());

  useEffect(() => {
    let sciChartSurface;

    const initializeChart = async () => {
      sciChartSurface = await createChart(rootElementId, data);
    };

    initializeChart();

    return () => {
      if (sciChartSurface) sciChartSurface.delete();
    };
  }, [data, rootElementId]);

  return <div id={rootElementId} style={{ width: "100%", height: "500px" }} />;
}

export default SciChart;
