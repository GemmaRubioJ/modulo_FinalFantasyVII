from odoo import api, models, fields
from datetime import date, datetime

class ShinraMember(models.Model):
    _name='ff7.shinra'
    name=fields.Char(required=True)
    birth=fields.Date()
    
class Turks(models.Model):
    _name = 'ff7.turks'
    name = fields.Char(required=True)
    birth = fields.Date()
    rank = fields.Char()
    #assassinated_member_id = fields.Many2one(comodel_name='ff7.avalanche', string='asesinado')

class SoldadoMember(models.Model):
    _name='ff7.soldado'
    name= fields.Char(required=True)
    birth = fields.Date()
    weapon = fields.Many2one(comodel_name='ff7.weapon', string='weapon')
    clase= fields.Selection([ ('first', 'Primera Clase'),('second', 'Segunda Clase'),], string='Clase')
    maddness_index = fields.Float(compute = '_compute_madness_index', store= True, index=True)
     
    @api.depends('weapon.materia_ids', 'weapon.materia_ids.materia_type')
    def _compute_madness_index(self):
        for record in self:
            madness_score = 0
            # Verificamos que el soldado tenga un arma asignada y que esta tenga materias.
            if record.weapon and record.weapon.materia_ids:
                for materia in record.weapon.materia_ids:
                    if materia.materia_type == 'invocation':
                        madness_score += 3
                    elif materia.materia_type == 'dark_magic':
                        madness_score += 2
                    elif materia.materia_type == 'support':
                        madness_score += 1
                    record.maddness_index = madness_score
            
class Avalanche(models.Model):
    _name='ff7.avalanche'
    name = fields.Char(required=True)
    #weapon_id = fields.Many2one(comodel_name='ff7.weapon', string='arma_especial')
    former_soldado = fields.Boolean()
    missions_count = fields.Integer()
    on_reserve = fields.Boolean(compute='_compute_on_reserve', readonly=True)
    reserve_time= fields.Date()
    #killer_turk = fields.One2many(comodel_name='ff7.turks', inverse_name='asesinado')
    
    @api.depends('missions_count')
    def _compute_on_reserve(self):
        for record in self:
            if record.missions_count >= 100:
                record.on_reserve = True
     
class Weapon(models.Model):
    _name='ff7.weapon'
    name = fields.Char(required=True)
    material = fields.Char()
    slot_count = fields.Float()
    materia_ids = fields.Many2many(comodel_name='ff7.materia', string='materias')
    #avalanche_owner= fields.One2many(comodel_name='ff7.avalanche', inverse_name='arma_especial')
    soldado_owner = fields.One2many(comodel_name='ff7.soldado', inverse_name='weapon')
    
class Materia(models.Model):
    _name='ff7.materia'
    name = fields.Char(required=True)
    materia_type = fields.Selection([('invocation', 'Invocación'), ('dark_magic', 'Magia Negra'), ('support', 'Apoyo')], string='Tipo')
    slot_occupancy = fields.Float()
    

