<template>
	<WbSubwidget titlecolor="var(--color-title)" :fullwidth="true">
		<template #title>
			<span class="vehiclename">{{ props.vehicle.name }} </span>
		</template>
		<div class="subgrid">
			<InfoItem heading="Status:" :small="false" class="grid-left grid-col-4">
				<span
					:style="{ color: statusColor }"
					class="d-flex justify-content-center align-items-center status-string"
					>{{ statusString }}</span
				>
			</InfoItem>
			<InfoItem heading="Ladestand:" :small="false" class="grid-col-4">
				{{ Math.round(props.vehicle.soc) }} %
			</InfoItem>
			<InfoItem
				heading="Reichweite:"
				:small="false"
				class="grid-right grid-col-4"
			>
				{{ props.vehicle.range }} km
			</InfoItem>
		</div>
	</WbSubwidget>
</template>
<script setup lang="ts">
import { computed } from 'vue'
import InfoItem from '../shared/InfoItem.vue'
import WbSubwidget from '../shared/WbSubwidget.vue'
import type { Vehicle } from '@/components/chargePointList/model.ts'

const props = defineProps<{
	vehicle: Vehicle
}>()

const statusString = computed(() => {
	let cp = props.vehicle.chargepoint
	if (cp != undefined) {
		let result = ''
		if (cp.isCharging) {
			result = 'Lädt (' + cp.name + ')'
		} else {
			result = 'Bereit (' + cp.name + ')'
		}
		return result
	} else {
		return 'Unterwegs'
	}
})

const statusColor = computed(() => {
	let cp = props.vehicle.chargepoint
	if (cp != undefined) {
		if (cp.isLocked) {
			return 'var(--color-evu)'
		} else if (cp.isCharging) {
			return 'var(--color-charging)'
		} else if (cp.isPluggedIn) {
			return 'var(--color-battery)'
		} else {
			return 'var(--color-axis)'
		}
	} else {
		return 'var(--color-axis)'
	}
})
</script>
<style scoped>
.idbadge {
	background-color: var(--color-menu);
	font-weight: normal;
}

.vehiclename {
	font-size: var(--font-large);
}
.status-string {
	text-align: center;
}
</style>
