import { InteractivePoints } from '../../InteractivePoints.js'
import { Area } from './Area.js'
import { projectsOnMain } from './projectsOnMain.js'

/**
 * World of Somnath — the junction of 8th Main and 4th Cross.
 * Somnath Nilaya (the hero building) is the door to the portfolio; the auto stand
 * is where rides to each project will start; the ten buildings along 8th Main each
 * open their case study.
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

        for(const project of projectsOnMain)
        {
            this.setPoint(`project${project.letter}Point`, `${project.n} ${project.title}`, () =>
            {
                window.open(`https://somnath.world/case/${project.slug}`, '_blank', 'noopener')
                this.game.notifications?.show?.(
                    `<div class="title">${project.n} · ${project.title}</div><p class="text">${project.kicker}. The case study opened in a new tab.</p>`,
                    'project',
                    4
                )
            })
        }
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
