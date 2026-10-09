import * as THREE from 'three/webgpu'
import { Game } from '../Game.js'

const clamp = (v, a, b) => Math.min(b, Math.max(a, v))
const damp = (current, target, lambda, dt) => current + (target - current) * (1 - Math.exp(- lambda * dt))

/**
 * Chikku — the companion who rides on the roof of your auto.
 * Built in blender/build_auto.py as a hierarchy under the chassis:
 *   companion (yaw) -> companionBody (hop, squash, lean)
 *                       -> companionEyes (blink), companionArmL / companionArmR (wave), companionLeaf (wobble)
 * Chikku turns to look at the nearest project, waves when you can open one,
 * hops when you honk, and bounces along with the ride.
 */
export class Companion
{
    constructor(visualVehicle)
    {
        this.game = Game.getInstance()

        const chassis = visualVehicle.parts.chassis
        this.root = chassis.getObjectByName('companion')
        if(!this.root)
            return

        this.body = chassis.getObjectByName('companionBody')
        this.eyes = chassis.getObjectByName('companionEyes')
        this.armL = chassis.getObjectByName('companionArmL')
        this.armR = chassis.getObjectByName('companionArmR')
        this.leaf = chassis.getObjectByName('companionLeaf')

        this.chassis = chassis
        this.bodyBaseY = this.body.position.y
        this.state = {
            yaw: 0,
            lean: 0,
            roll: 0,
            hop: 0,
            hopVelocity: 0,
            squash: 0,
            wave: 0,
            blinkTimer: 2 + Math.random() * 3,
            blink: 0,
            glanceTimer: 4,
            glance: 0,
            lastForwardSpeed: 0,
            lastYaw: null,
            wasActive: false,
        }
        this.lookWorld = new THREE.Vector3()
        this.lookLocal = new THREE.Vector3()

        this.game.inputs?.events?.on('honk', (action) =>
        {
            if(action.active)
                this.jump(3.2)
        })

        this.game.ticker.events.on('tick', () =>
        {
            this.update()
        }, 9)

        window.__chikku = this
    }

    jump(strength = 2.6)
    {
        if(this.state.hop < 0.02)
            this.state.hopVelocity = strength
    }

    update()
    {
        const dt = Math.min(this.game.ticker.deltaScaled, 0.05)
        if(!dt)
            return
        const t = this.game.ticker.elapsedScaled
        const s = this.state
        const vehicle = this.game.physicalVehicle
        const speed = vehicle?.xzSpeed || 0
        const forwardSpeed = vehicle?.forwardSpeed || 0
        const speedFactor = clamp(speed / 10, 0, 1)

        // Acceleration and turn rate (in the chassis frame)
        const acceleration = (forwardSpeed - s.lastForwardSpeed) / dt
        s.lastForwardSpeed = forwardSpeed
        const yaw = this.chassis.rotation.y
        let yawRate = 0
        if(s.lastYaw !== null)
        {
            let d = yaw - s.lastYaw
            if(d > Math.PI) d -= Math.PI * 2
            if(d < - Math.PI) d += Math.PI * 2
            yawRate = d / dt
        }
        s.lastYaw = yaw

        // Lean back when accelerating, forward when braking; lean out of turns
        s.lean = damp(s.lean, clamp(- acceleration * 0.035, - 0.4, 0.4), 6, dt)
        s.roll = damp(s.roll, clamp(yawRate * speedFactor * 0.22, - 0.35, 0.35), 5, dt)

        // Look at the nearest project (or anything interactive) within 16 m
        let target = 0
        let nearest = Infinity
        const player = this.game.player?.position2 || { x: 1e6, y: 1e6 }
        for(const item of (this.game.interactivePoints?.items || []))
        {
            const d = Math.hypot(item.position.x - player.x, item.position.y - player.y)
            if(d < 16 && d < nearest)
            {
                nearest = d
                this.lookWorld.set(item.position.x, this.chassis.position.y, item.position.y)
            }
        }
        if(nearest < Infinity)
        {
            this.lookLocal.copy(this.lookWorld)
            this.chassis.worldToLocal(this.lookLocal)
            this.lookLocal.sub(this.root.position)
            target = clamp(Math.atan2(- this.lookLocal.z, this.lookLocal.x), - 2.2, 2.2)
        }
        else
        {
            // idle: glance around now and then
            s.glanceTimer -= dt
            if(s.glanceTimer < 0)
            {
                s.glance = s.glance === 0 ? (Math.random() < 0.5 ? - 1 : 1) * (0.6 + Math.random() * 0.8) : 0
                s.glanceTimer = s.glance === 0 ? 3 + Math.random() * 4 : 1.2 + Math.random()
            }
            target = s.glance * (1 - speedFactor)
        }
        s.yaw = damp(s.yaw, target, 5, dt)

        // Wave when a point is in reach; little celebration hop the moment one becomes active
        const active = !!this.game.interactivePoints?.activeItem
        if(active && !s.wasActive)
            this.jump(2.4)
        s.wasActive = active
        s.wave = damp(s.wave, active ? 1 : 0, 7, dt)

        // Hop physics (ride bumps feed small hops)
        if(speed > 3 && s.hop < 0.005 && Math.random() < dt * speedFactor * 2.2)
            this.jump(0.9 + Math.random() * 0.6 * speedFactor)
        s.hopVelocity -= 14 * dt
        s.hop += s.hopVelocity * dt
        if(s.hop < 0)
        {
            if(s.hopVelocity < - 1)
                s.squash = clamp(- s.hopVelocity * 0.06, 0, 0.3)
            s.hop = 0
            s.hopVelocity = 0
        }
        s.squash = damp(s.squash, 0, 9, dt)

        // Blink
        s.blinkTimer -= dt
        if(s.blinkTimer < 0)
        {
            s.blink = 1
            s.blinkTimer = 2.2 + Math.random() * 3.5
        }
        s.blink = damp(s.blink, 0, 18, dt)

        // Apply
        const breathe = Math.sin(t * 2.4) * 0.025
        const stretch = s.hopVelocity > 0 ? clamp(s.hopVelocity * 0.03, 0, 0.12) : 0
        const sy = 1 + breathe - s.squash + stretch
        const sxz = 1 - breathe * 0.6 + s.squash * 0.7 - stretch * 0.5

        this.root.rotation.y = s.yaw
        this.body.position.y = this.bodyBaseY + s.hop
        this.body.scale.set(sxz, sy, sxz)
        this.body.rotation.z = s.lean
        this.body.rotation.x = s.roll

        if(this.eyes)
            this.eyes.scale.y = 1 - s.blink * 0.9

        const swing = Math.sin(t * 9) * 0.25 * speedFactor
        if(this.armL)
            this.armL.rotation.x = - (s.wave * (2.3 + Math.sin(t * 13) * 0.4)) - 0.15 - swing
        if(this.armR)
            this.armR.rotation.x = 0.15 + swing + s.squash * 0.8

        if(this.leaf)
        {
            this.leaf.rotation.z = Math.sin(t * 11) * 0.12 * (0.3 + speedFactor) - s.lean * 0.8
            this.leaf.rotation.x = Math.sin(t * 7.3) * 0.1 + s.roll * 0.8
        }
    }
}
