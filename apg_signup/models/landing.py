from odoo import api, fields, models, exceptions,_
from odoo.exceptions import UserError, ValidationError
import json

class ColourCombination(models.Model):
    _name = 'colour.combination'
    _description = 'Colour Combination'

    name = fields.Char("Name")
    primary_color = fields.Char(string="Primary Color")
    secondary_color = fields.Char(string="Secondary Color")
    text_color = fields.Char(string="Default Text Color", default="#ffffff")
    background_color = fields.Char(string="Default Background Color", default="#000000")

    @api.depends('primary_color', 'secondary_color', 'text_color', 'background_color')
    def _compute_colors_json(self):
        for record in self:
            record.colors_json = json.dumps([
                record.primary_color or "#044e99",
                record.secondary_color or "#FFD000",
                record.text_color or "#FFFFFF",
                record.background_color or "#000000"
            ])

    colors_json = fields.Char(compute='_compute_colors_json', store=False)

class Courses(models.Model):
    _name = 'course.course'
    _description = 'Courses'

    image = fields.Binary(string='Image')
    name = fields.Char(string="Name")

class SlideChannel(models.Model):
    _inherit = 'slide.channel'
    _description = 'Creator Landing Page'

    # Topbar
    p1 = fields.Char(string="Topbar Title", default="Unlimited Lifetime Access. Starting at INR")
    price1 = fields.Integer(string="Amount")
    price2 = fields.Integer(string="Amount")
    combination_id = fields.Many2one('colour.combination', string="Colour Combination")
    primary_color = fields.Char(string="Primary Color")
    secondary_color = fields.Char(string="Secondary Color")

    # Main Heading
    creator_name = fields.Char(string="Creator Name")
    image_icon = fields.Binary(string="Creator Image")
    main_heading = fields.Char(string="Title")
    p2 = fields.Text(string="Content")

    c1 = fields.Char(string="USP Content")
    c2 = fields.Char(string="USP Content")
    c3 = fields.Char(string="USP Content", default="Life Time Access")
    c4 = fields.Char(string="USP Content", default="LIVE QnA Sessions")

    # ABOUT THIS COURSE
    course_title = fields.Char(string="Title", default="ABOUT THIS COURSE")
    course_line_ids = fields.One2many('about.course', 'landing_id')
    # p3 = fields.Text(string="Content")

    #WHAT AN INDIVIDUAL CAN LEARN FROM THIS?
    h1 = fields.Char(string="Title", default="WHAT AN INDIVIDUAL CAN LEARN FROM THIS?")
    individual_line_ids = fields.One2many('individual.learn', 'landing_id')
    
    #COURSE CURRICULUM
    h2 = fields.Char(string="Title", default="COURSE CURRICULUM")
    line_ids = fields.One2many('course.curriculum.line', 'landing_id')

    #ABOUT ME
    h3 = fields.Char(string="Title", default="ABOUT ME")
    about_me_line_ids = fields.One2many('about.me', 'landing_id')
    my_image_icon = fields.Binary(string="Creator Image")
    # c10 = fields.Text(string="Content")
    m1 = fields.Char(string="Facebook")
    m2 = fields.Char(string="Social-Media X")
    m3 = fields.Char(string="Linkedin")
    m4 = fields.Char(string="Youtube")
    m5 = fields.Char(string="Instagram")
    m6 = fields.Char(string="pinterest")

    #WHO SHOULD TAKE THIS COURSE?
    h6 = fields.Char(string="Title", default="WHO SHOULD TAKE THIS COURSE ?")
    course_ids = fields.Many2many('course.course')

    #FROM OUR STUDENTS
    h7 = fields.Char(string="Title", default="FROM OUR STUDENTS")
    c12 = fields.Text(string="Content", default="We make every moment count with solutions designed just for you.")
    student_line_ids = fields.One2many('our.student.line', 'landing_id')

    #The Complete Guide To Starting Up
    h4 = fields.Char(string="Title")
    c11 = fields.Text(string="Content")
    image1 = fields.Binary(string="Image")

    #FREQUENTLY ASKED QUESTIONS
    h5 = fields.Char(string="Title", default="FREQUENTLY ASKED QUESTIONS")
    faq_ids = fields.One2many('frequently.ask.question', 'landing_id')


    #certificate course fields
    is_this_certificate_course = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string="Is This Certificate Course?")
    issued_by = fields.Char(string="Certificate Issued By?")
    upload_signature = fields.Binary(string="Upload Signature")

    #Course Thumbnail
    # browse_file = fields.Binary(string="Course Thumbnail")



class CourseCurriculumLine(models.Model):
    _name = 'course.curriculum.line'
    _description = 'Course Curriculum Line'

    landing_id = fields.Many2one('slide.channel')
    h1 = fields.Char(string="Title")
    c1 = fields.Text(string="Content")

class FrequentlyAskQuestion(models.Model):
    _name = 'frequently.ask.question'
    _description = 'Frequently Ask Question'

    landing_id = fields.Many2one('slide.channel')
    q1 = fields.Char(string="Question")
    a1 = fields.Text(string="Answer")

class AboutCourse(models.Model):
    _name = 'about.course'
    _description = 'About Course'

    landing_id = fields.Many2one('slide.channel')
    p1 = fields.Char(string="Content")

class AboutMe(models.Model):
    _name = 'about.me'
    _description = 'About Course'

    landing_id = fields.Many2one('slide.channel')
    p1 = fields.Char(string="Content")

class OurStudent(models.Model):
    _name = 'our.student.line'
    _description = 'Our Student Line'

    landing_id = fields.Many2one('slide.channel')
    name = fields.Char(string="Name")
    content_type = fields.Selection([
        ('text', 'Text'),
        ('video', 'Video'),
        ],string="Content Type")
    p1 = fields.Text(string="Content")
    v1 = fields.Char(string="Video")
    rating = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ])
    image = fields.Binary('Image')

class IndividualCanLearn(models.Model):
    _name = 'individual.learn'
    _description = 'What an Individual can Learn From This'

    landing_id = fields.Many2one('slide.channel')
    c1 = fields.Text(string="Content")
