<template>
	<p class="settingsheader mt-2 ms-1">Preisbasiertes Laden:</p>
	<p class="providername ms-1">Anbieter: {{ etData.etProvider }}</p>
	<hr />
	<div class="row p-0 m-0">
		<div class="col-12 pricechartColumn p-0 m-0">
			<figure id="pricechart" class="p-0 m-0">
				<svg viewBox="0 0 400 300">
					<g
						:id="chartId"
						:origin="draw"
						:transform="'translate(' + margin.top + ',' + margin.right + ')'"
					/>
				</svg>
			</figure>
		</div>
	</div>

	<div v-if="chargepoint != undefined" class="p-3">
		<RangeInput
			v-if="chargepoint.etActive"
			id="foo"
			v-model="maxPrice"
			:min="-25"
			:max="95"
			:step="0.1"
			:decimals="1"
			unit="ct"
		/>
	</div>
	<div v-if="chargepoint != undefined" class="d-flex justify-content-end">
		<span class="me-3 pt-0" @click="setMaxPrice">
			<button
				type="button"
				class="btn btn-secondary"
				:style="confirmButtonStyle"
				:disabled="!maxPriceEdited"
			>
				Bestätigen
			</button>
		</span>
	</div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { etData } from './model'
import {
	extent,
	scaleTime,
	scaleLinear,
	line,
	axisBottom,
	timeFormat,
	axisLeft,
	select,
} from 'd3'
import RangeInput from '../shared/RangeInput.vue'
import { chargePoints, type ChargePoint } from '../chargePointList/model'
const props = defineProps<{
	chargepoint?: ChargePoint
	globalview?: boolean
}>()

let _maxPrice = props.chargepoint ? ref(props.chargepoint.etMaxPrice) : ref(0)
const maxPriceEdited = ref(false)
const cp = ref(props.chargepoint)
const maxPrice = computed({
	get() {
		return _maxPrice.value
		// ref(props.chargepoint.etMaxPrice)
	},
	set(newmax) {
		_maxPrice.value = newmax
		maxPriceEdited.value = true
	},
})

function setMaxPrice() {
	if (cp.value) {
		chargePoints[cp.value.id].etMaxPrice = maxPrice.value
	}
	maxPriceEdited.value = false
}
const needsUpdate = ref(false)
let dummy = false
const width = 400
const height = 250
const margin = { top: 0, bottom: 15, left: 20, right: 5 }
const axisfontsize = 12
const plotdata = computed(() => {
	let valueArray: [Date, number][] = []
	if (etData.etPriceList.size > 0) {
		etData.etPriceList.forEach((value, date) => {
			valueArray.push([date, value])
		})
	}
	return valueArray
})
const barwidth = computed(() => {
	if (plotdata.value.length > 1) {
		return (width - margin.left - margin.right) / plotdata.value.length - 1
	} else {
		return 0
	}
})
const confirmButtonStyle = computed(() => {
	if (maxPriceEdited.value) {
		return { background: 'var(--color-charging)' }
	} else {
		return { background: 'var(--color-menu)' }
	}
})
const xScale = computed(() => {
	let xdomain = extent(plotdata.value, (d) => d[0]) as [Date, Date]

	return scaleTime()
		.range([margin.left, width - margin.left - margin.right])
		.domain(xdomain)
})
const yDomain = computed(() => {
	let yd = extent(plotdata.value, (d) => d[1]) as [number, number]
	yd[0] = Math.floor(yd[0] - 1)
	yd[1] = Math.floor(yd[1] + 1)
	return yd
})
const yScale = computed(() => {
	return scaleLinear()
		.range([height - margin.bottom, 0])
		.domain(yDomain.value)
})
const linePath = computed(() => {
	const generator = line()
	const points = [
		[margin.left, yScale.value(maxPrice.value)],
		[width - margin.right, yScale.value(maxPrice.value)],
	]
	return generator(points as [number, number][])
})
const zeroPath = computed(() => {
	const generator = line()
	const points = [
		[margin.left, yScale.value(0)],
		[width - margin.right, yScale.value(0)],
	]
	return generator(points as [number, number][])
})

const xAxisGenerator = computed(() => {
	return axisBottom<Date>(xScale.value)
		.ticks(6)
		.tickSize(5)
		.tickFormat(timeFormat('%H:%M'))
})
const yAxisGenerator = computed(() => {
	return axisLeft<number>(yScale.value)
		.ticks(6)
		.tickSizeInner(-(width - margin.right - margin.left))
		.tickFormat((d) => d.toString())
})
const draw = computed(() => {
	if (needsUpdate.value == true) {
		dummy = !dummy
	}

	const svg = select('g#' + chartId.value)
	svg.selectAll('*').remove()
	const bargroups = svg
		.selectAll('bar')
		.data(plotdata.value)
		.enter()
		.append('g')
	bargroups
		.append('rect')
		.attr('class', 'bar')
		.attr('x', (d) => xScale.value(d[0]))
		.attr('y', (d) => yScale.value(d[1]))
		.attr('width', barwidth.value)
		.attr('height', (d) => yScale.value(yDomain.value[0]) - yScale.value(d[1]))
		.attr('fill', (d) =>
			d[1] <= maxPrice.value ? 'var(--color-charging)' : 'var(--color-axis)',
		)
	// X Axis
	const xAxis = svg.append('g').attr('class', 'axis').call(xAxisGenerator.value)
	xAxis.attr('transform', 'translate(0,' + (height - margin.bottom) + ')')
	xAxis
		.selectAll('.tick')
		.attr('font-size', axisfontsize)
		.attr('color', 'var(--color-bg)')
	xAxis
		.selectAll('.tick line')
		.attr('stroke', 'var(--color-fg)')
		.attr('stroke-width', '0.5')
	xAxis.select('.domain').attr('stroke', 'var(--color-bg')
	// Y Axis
	const yAxis = svg.append('g').attr('class', 'axis').call(yAxisGenerator.value)
	yAxis.attr('transform', 'translate(' + margin.left + ',' + 0 + ')')
	yAxis
		.selectAll('.tick')
		.attr('font-size', axisfontsize)
		.attr('color', 'var(--color-bg)')

	yAxis
		.selectAll('.tick line')
		.attr('stroke', 'var(--color-bg)')
		.attr('stroke-width', '0.5')
	yAxis.select('.domain').attr('stroke', 'var(--color-bg)')
	// zero line
	if (yDomain.value[0] < 0) {
		svg
			.append('path')
			.attr('d', zeroPath.value)
			.attr('stroke', 'var(--color-fg)')
	}
	// Line for max price
	svg.append('path').attr('d', linePath.value).attr('stroke', 'yellow')

	return 'PriceChart.vue'
})
const chartId = computed(() => {
	if (props.chargepoint) {
		return 'priceChartCanvas' + props.chargepoint.id
	} else {
		return 'priceChartCanvasGlobal'
	}
})
onMounted(() => {
	needsUpdate.value = !needsUpdate.value
})
</script>

<style scoped>
.color-charging {
	color: var(--color-charging);
}

.fa-circle-check {
	color: var(--color-menu);
}

.settingsheader {
	color: var(--color-charging);
	font-size: 16px;
	font-weight: bold;
}

.providername {
	color: var(--color-axis);
	font-size: 16px;
}
</style>
