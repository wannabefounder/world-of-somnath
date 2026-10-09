import * as THREE from 'three/webgpu'
import { Cycles } from './Cycles.js'

const presets = {
    // World of Somnath: Bengaluru light. Warm sun, cool blue-grey shadows, dusty haze; signboard-yellow reveal.
    day:   { revealColor: new THREE.Color('#f5c400'), revealIntensity: 6, electricField: 0, temperature: 4, lightColor: new THREE.Color('#fff0d8'), lightIntensity: 1.15, shadowColor: new THREE.Color('#5a6894'), fogColorA: new THREE.Color('#cfe6ef'), fogColorB: new THREE.Color('#f3d9b4'), fogNearRatio: 0.315, fogFarRatio: 1.25 },
    dusk:  { revealColor: new THREE.Color('#ffb02e'), revealIntensity: 5, electricField: 0.15, temperature: 1, lightColor: new THREE.Color('#ffb07a'), lightIntensity: 1.2, shadowColor: new THREE.Color('#5c3f7a'), fogColorA: new THREE.Color('#f08a5d'), fogColorB: new THREE.Color('#ffcf8f'), fogNearRatio: 0.05, fogFarRatio: 1.25 },
    night: { revealColor: new THREE.Color('#f5c400'), revealIntensity: 8, electricField: 0.6, temperature: -5, lightColor: new THREE.Color('#7d86c4'), lightIntensity: 1.9, shadowColor: new THREE.Color('#1c2252'), fogColorA: new THREE.Color('#111a3a'), fogColorB: new THREE.Color('#2c2142'), fogNearRatio: -0.6, fogFarRatio: 1 },
    dawn:  { revealColor: new THREE.Color('#ffc46b'), revealIntensity: 4.85, electricField: 0.15, temperature: 1, lightColor: new THREE.Color('#ffc49a'), lightIntensity: 1.15, shadowColor: new THREE.Color('#6a4a72'), fogColorA: new THREE.Color('#ffd7b8'), fogColorB: new THREE.Color('#f5a27c'), fogNearRatio: 0.3, fogFarRatio: 1.25 },
}

export class DayCycles extends Cycles
{
    constructor()
    {
        const forcedProgress = import.meta.env.VITE_DAY_CYCLE_PROGRESS ? parseFloat(import.meta.env.VITE_DAY_CYCLE_PROGRESS) : null
        super('🕜 Day Cycles', 4 * 60, forcedProgress, false)
    }

    // World of Somnath: the sky follows the live time in Bengaluru (IST, UTC+5:30).
    // IST hours are mapped onto the engine's keyframes: day until 16:00, dusk around 18:30,
    // night from 20:00 to 04:30, dawn around 06:00, full day again by 07:30.
    realProgress()
    {
        const istMs = Date.now() + 5.5 * 3600 * 1000
        const hours = (istMs / 3600000) % 24
        // [IST hour, progress] — progress 0 is 10:00
        const map = [ [ 10, 0 ], [ 16, 0.15 ], [ 18.5, 0.25 ], [ 20, 0.35 ], [ 28.5, 0.6 ], [ 30, 0.8 ], [ 31.5, 0.9 ], [ 34, 1 ] ]
        const h = hours < 10 ? hours + 24 : hours
        let fraction = 0
        for(let i = 0; i < map.length - 1; i++)
        {
            const [ h0, p0 ] = map[i], [ h1, p1 ] = map[i + 1]
            if(h >= h0 && h <= h1) { fraction = p0 + (p1 - p0) * (h - h0) / (h1 - h0); break }
        }
        const dayIndex = Math.floor((istMs - 10 * 3600000) / 86400000)
        return dayIndex + fraction
    }

    get presets()
    {
        return presets
    }

    getKeyframesDescriptions()
    {
        // Debug
        if(this.game.debug.active)
        {
            this.debugPanel.addBinding(this, 'duration', { min: 1, max: 60 * 10, step: 1 })

            for(const presetKey in presets)
            {
                const preset = presets[presetKey]
                const presetsDebugPanel = this.debugPanel.addFolder({
                    title: presetKey,
                    expanded: true,
                })

                this.game.debug.addThreeColorBinding(presetsDebugPanel, preset.revealColor, 'revealColor')
                presetsDebugPanel.addBinding(preset, 'revealIntensity', { min: 0, max: 20, step: 0.001 })
                this.game.debug.addThreeColorBinding(presetsDebugPanel, preset.lightColor, 'lightColor')
                presetsDebugPanel.addBinding(preset, 'lightIntensity', { min: 0, max: 20 })
                this.game.debug.addThreeColorBinding(presetsDebugPanel, preset.shadowColor, 'shadowColor')
                this.game.debug.addThreeColorBinding(presetsDebugPanel, preset.fogColorA, 'fogColorA')
                this.game.debug.addThreeColorBinding(presetsDebugPanel, preset.fogColorB, 'fogColorB')
                presetsDebugPanel.addBinding(preset, 'fogNearRatio', { label: 'near', min: -2, max: 2, step: 0.001 })
                presetsDebugPanel.addBinding(preset, 'fogFarRatio', { label: 'far', min: -2, max: 2, step: 0.001 })
            }
        }

        return [
            [
                { properties: presets.day, stop: 0.0 }, // day
                { properties: presets.day, stop: 0.15 }, // day
                { properties: presets.dusk, stop: 0.25 }, // Dusk
                { properties: presets.night, stop: 0.35 }, // Night
                { properties: presets.night, stop: 0.6 }, // Night
                { properties: presets.dawn, stop: 0.8 }, // Dawn
                { properties: presets.day, stop: 0.9 }, // day
            ]
        ]
    }

    getIntervalDescriptions()
    {
        return [
            { name: 'night', start: 0.25, end: 0.7 },
            { name: 'deepNight', start: 0.35, end: 0.6 },
        ]
    }
}