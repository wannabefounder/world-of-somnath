import { InteractivePoints } from '../../InteractivePoints.js'
import { Area } from './Area.js'

/**
 * World of Somnath — the junction of 8th Main and 4th Cross.
 * Somnath Nilaya (the hero building) is the door to the portfolio; the auto stand
 * is where rides to each project will start.
 */
export class HomeArea extends Area
{
    constructor(model)
    {
        super(model)

        this.setPoint('heroInteractivePoint', 'See my work', () =>
        {
            window.open('https://somnath.world/work', '_blank', 'noopener')
        })

        this.setPoint('autoStandInteractivePoint', 'Auto stand', () =>
        {
            this.game.notifications?.show?.(
                '<div class="title">Auto stand</div><p class="text">Meter rides to every project start here soon. For now, the auto is yours: drive around.</p>',
                'auto-stand',
                5
            )
        })
    }

    setPoint(referenceName, label, onInteract)
    {
        const references = this.references.items.get(referenceName)
        if(!references || !references.length)
            return

        this.game.interactivePoints.create(
            references[0].position,
            label,
            InteractivePoints.ALIGN_RIGHT,
            InteractivePoints.STATE_CONCEALED,
            () =>
            {
                this.game.inputs.interactiveButtons.clearItems()
                onInteract()
            },
            () =>
            {
                this.game.inputs.interactiveButtons.addItems([ 'interact' ])
            },
            () =>
            {
                this.game.inputs.interactiveButtons.removeItems([ 'interact' ])
            },
            () =>
            {
                this.game.inputs.interactiveButtons.removeItems([ 'interact' ])
            }
        )
    }
}
