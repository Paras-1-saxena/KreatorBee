# custom_module/controllers/referral.py 
from cryptography.fernet import Fernet
import base64
import logging
import werkzeug
from werkzeug.urls import url_encode
import requests
from datetime import datetime,date
from odoo import http, tools, _
from odoo import fields
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.payment.controllers import portal as payment_portal
from odoo.exceptions import UserError, ValidationError
from odoo.http import request, route
import odoo.exceptions
from odoo.exceptions import AccessError
from odoo.service import security
from odoo.tools.translate import _
import pytz
import re

class ForumSection(http.Controller):
    @http.route('/forumsection', type='http', auth='public', website=True)
    def forumpost(self, **kwargs):
        pattern = r'(?:v=|/v/|youtu\.be/|embed/)([a-zA-Z0-9_-]{11})'
        post_obj = request.env['apg.social.post']
        user_id = request.env.user.id
        user_type = request.env.user.partner_id.user_type
        posts = post_obj.sudo().search([('partner_type','=', 'creator')], order='create_date desc')
        user_tz = request.env.user.tz or 'UTC'  # Get the user's timezone, default to UTC
        local_tz = pytz.timezone(user_tz)  # Convert to timezone object

        post_data = []
        for post in posts:
            # Fetch like status and comments for each post
            is_liked = bool(request.env['apg.post.like'].sudo().search([('post_id', '=', post.id), ('create_uid', '=', user_id)], limit=1))
            # comments = request.env['apg.post.comment'].sudo().search([('post_id', '=', post.id)])
            
            # Convert create_date to user's timezone
            create_date_utc = post.create_date.replace(tzinfo=pytz.utc)  # Ensure it's in UTC
            create_date_local = create_date_utc.astimezone(local_tz)  # Convert to local timezone
            create_date = create_date_local.strftime('%B %d, %Y, %I:%M %p')
            print("create_date",create_date)
            videoID = False
            media_files = []
            if post.video_url:
                match = re.search(pattern, post.video_url)
                if match:
                    videoID = match.group(1)
            for img in post.image_ids:
                # Base64 encode the media content
                media_files.append({
                    'image': img,
                    'type': img.mimetype.split("/")[0],  # 'image' or 'video'
                    'mimetype': img.mimetype,  # Full MIME type (e.g., 'image/png', 'video/mp4')
                })
            
            # Add post data
            post_data.append({
                'id': post.id,
                'post_id': post,
                'message': post.message,
                'create_uid': post.create_uid.name,
                'create_date': create_date,
                'is_liked': is_liked,
                'media': media_files,  # Pass media files here
                'video_url': 'https://www.youtube.com/embed/'+str(videoID) if videoID else False,
                'comments': self.get_comments(post)
                # [
                #     {
                #         'user': comment.create_uid.name,
                #         'message': comment.message,
                #         'date': datetime.strftime(
                #             comment.create_date.replace(tzinfo=pytz.utc).astimezone(local_tz), '%B %d, %Y, %I:%M %p'),
                #         'id': comment.id,
                #     } for comment in comments
                # ],
            })
        values = {'post_ids': post_data,'user_type':user_type}
        return http.request.render('apg_social_media.fbpostforum', values)

    # Partner Community Menu URLS START
    @http.route('/forumsection-partner', type='http', auth='public', website=True)
    def partner_forumpost(self, **kwargs):
        pattern = r'(?:v=|/v/|youtu\.be/|embed/)([a-zA-Z0-9_-]{11})'
        post_obj = request.env['apg.social.post']
        user_id = request.env.user.id
        user_type = request.env.user.partner_id.user_type
        partner_type = 'partner'
        posts = post_obj.sudo().search([('partner_type','=', partner_type)], order='create_date desc')
        user_tz = request.env.user.tz or 'UTC'  # Get the user's timezone, default to UTC
        local_tz = pytz.timezone(user_tz)  # Convert to timezone object

        post_data = []
        for post in posts:
            # Fetch like status and comments for each post
            is_liked = bool(request.env['apg.post.like'].sudo().search([('post_id', '=', post.id), ('create_uid', '=', user_id)], limit=1))
            comments = request.env['apg.post.comment'].sudo().search([('post_id', '=', post.id)])
            
            # Convert create_date to user's timezone
            create_date_utc = post.create_date.replace(tzinfo=pytz.utc)  # Ensure it's in UTC
            create_date_local = create_date_utc.astimezone(local_tz)  # Convert to local timezone
            create_date = create_date_local.strftime('%B %d, %Y, %I:%M %p')
            print("create_date",create_date)
            videoID = False
            media_files = []
            if post.video_url:
                match = re.search(pattern, post.video_url)
                if match:
                    videoID = match.group(1)
            for img in post.image_ids:
                # Base64 encode the media content
                media_files.append({
                    'image': img,
                    'type': img.mimetype.split("/")[0],  # 'image' or 'video'
                    'mimetype': img.mimetype,  # Full MIME type (e.g., 'image/png', 'video/mp4')
                })
            
            # Add post data
            post_data.append({
                'id': post.id,
                'post_id': post,
                'message': post.message,
                'create_uid': post.create_uid.name,
                'create_date': create_date,
                'is_liked': is_liked,
                'media': media_files,  # Pass media files here
                'video_url': 'https://www.youtube.com/embed/'+str(videoID) if videoID else False,
                'comments': self.get_comments(post)
                # 'comments': [
                #     {
                #         'user': comment.create_uid.name,
                #         'message': comment.message,
                #         'date': datetime.strftime(
                #             comment.create_date.replace(tzinfo=pytz.utc).astimezone(local_tz), '%B %d, %Y, %I:%M %p')
                #     } for comment in comments
                # ],
            })
        values = {'post_ids': post_data,'user_type':user_type, 'partner_type':partner_type}
        return http.request.render('apg_social_media.fbpostforum_partner', values)

    @http.route('/forumsection-creator', type='http', auth='public', website=True)
    def creator_forumpost(self, **kwargs):
        pattern = r'(?:v=|/v/|youtu\.be/|embed/)([a-zA-Z0-9_-]{11})'
        post_obj = request.env['apg.social.post']
        user_id = request.env.user.id
        user_type = request.env.user.partner_id.user_type
        partner_type = 'creator'
        posts = post_obj.sudo().search([('partner_type','=', partner_type)], order='create_date desc')
        user_tz = request.env.user.tz or 'UTC'  # Get the user's timezone, default to UTC
        local_tz = pytz.timezone(user_tz)  # Convert to timezone object

        post_data = []
        for post in posts:
            # Fetch like status and comments for each post
            is_liked = bool(request.env['apg.post.like'].sudo().search([('post_id', '=', post.id), ('create_uid', '=', user_id)], limit=1))
            comments = request.env['apg.post.comment'].sudo().search([('post_id', '=', post.id)])
            
            # Convert create_date to user's timezone
            create_date_utc = post.create_date.replace(tzinfo=pytz.utc)  # Ensure it's in UTC
            create_date_local = create_date_utc.astimezone(local_tz)  # Convert to local timezone
            create_date = create_date_local.strftime('%B %d, %Y, %I:%M %p')
            print("create_date",create_date)
            videoID = False
            media_files = []
            if post.video_url:
                match = re.search(pattern, post.video_url)
                if match:
                    videoID = match.group(1)
            for img in post.image_ids:
                # Base64 encode the media content
                media_files.append({
                    'image': img,
                    'type': img.mimetype.split("/")[0],  # 'image' or 'video'
                    'mimetype': img.mimetype,  # Full MIME type (e.g., 'image/png', 'video/mp4')
                })
            
            # Add post data
            post_data.append({
                'id': post.id,
                'post_id': post,
                'message': post.message,
                'create_uid': post.create_uid.name,
                'create_date': create_date,
                'is_liked': is_liked,
                'media': media_files,  # Pass media files here
                'video_url': 'https://www.youtube.com/embed/'+str(videoID) if videoID else False,
                'comments': self.get_comments(post)
                # 'comments': [
                #     {
                #         'user': comment.create_uid.name,
                #         'message': comment.message,
                #         'date': datetime.strftime(
                #             comment.create_date.replace(tzinfo=pytz.utc).astimezone(local_tz), '%B %d, %Y, %I:%M %p')
                #     } for comment in comments
                # ],
            })
        values = {'post_ids': post_data,'user_type':user_type, 'partner_type':partner_type}
        return http.request.render('apg_social_media.fbpostforum_partner', values)

    @http.route('/forumsection-company', type='http', auth='public', website=True)
    def company_forumpost(self, **kwargs):
        pattern = r'(?:v=|/v/|youtu\.be/|embed/)([a-zA-Z0-9_-]{11})'
        post_obj = request.env['apg.social.post']
        user_id = request.env.user.id
        user_type = request.env.user.partner_id.user_type
        partner_type = 'company'
        posts = post_obj.sudo().search([('partner_type','=', partner_type)], order='create_date desc')
        user_tz = request.env.user.tz or 'UTC'  # Get the user's timezone, default to UTC
        local_tz = pytz.timezone(user_tz)  # Convert to timezone object

        post_data = []
        for post in posts:
            # Fetch like status and comments for each post
            is_liked = bool(request.env['apg.post.like'].sudo().search([('post_id', '=', post.id), ('create_uid', '=', user_id)], limit=1))
            comments = request.env['apg.post.comment'].sudo().search([('post_id', '=', post.id)])
            
            # Convert create_date to user's timezone
            create_date_utc = post.create_date.replace(tzinfo=pytz.utc)  # Ensure it's in UTC
            create_date_local = create_date_utc.astimezone(local_tz)  # Convert to local timezone
            create_date = create_date_local.strftime('%B %d, %Y, %I:%M %p')
            print("create_date",create_date)
            videoID = False
            media_files = []
            if post.video_url:
                match = re.search(pattern, post.video_url)
                if match:
                    videoID = match.group(1)
            for img in post.image_ids:
                # Base64 encode the media content
                media_files.append({
                    'image': img,
                    'type': img.mimetype.split("/")[0],  # 'image' or 'video'
                    'mimetype': img.mimetype,  # Full MIME type (e.g., 'image/png', 'video/mp4')
                })
            
            # Add post data
            post_data.append({
                'id': post.id,
                'post_id': post,
                'message': post.message,
                'create_uid': post.create_uid.name,
                'create_date': create_date,
                'is_liked': is_liked,
                'media': media_files,  # Pass media files here
                'video_url': 'https://www.youtube.com/embed/'+str(videoID) if videoID else False,
                'comments': self.get_comments(post)
                # 'comments': [
                #     {
                #         'user': comment.create_uid.name,
                #         'message': comment.message,
                #         'date': datetime.strftime(
                #             comment.create_date.replace(tzinfo=pytz.utc).astimezone(local_tz), '%B %d, %Y, %I:%M %p')
                #     } for comment in comments
                # ],
            })
        values = {'post_ids': post_data,'user_type':user_type, 'partner_type':partner_type}
        return http.request.render('apg_social_media.fbpostforum_partner', values)

    # Partner Community Menu URLS END

    # Customer Community Menu URLS END
    @http.route('/forumsection-customer', type='http', auth='public', website=True)
    def customer_forumpost(self, **kwargs):
        pattern = r'(?:v=|/v/|youtu\.be/|embed/)([a-zA-Z0-9_-]{11})'
        post_obj = request.env['apg.social.post']
        user_id = request.env.user.id
        user_type = request.env.user.partner_id.user_type
        partner_type = 'company'
        posts = post_obj.sudo().search([('partner_type','=', partner_type)], order='create_date desc')
        user_tz = request.env.user.tz or 'UTC'  # Get the user's timezone, default to UTC
        local_tz = pytz.timezone(user_tz)  # Convert to timezone object

        post_data = []
        for post in posts:
            # Fetch like status and comments for each post
            is_liked = bool(request.env['apg.post.like'].sudo().search([('post_id', '=', post.id), ('create_uid', '=', user_id)], limit=1))
            comments = request.env['apg.post.comment'].sudo().search([('post_id', '=', post.id)])
            
            # Convert create_date to user's timezone
            create_date_utc = post.create_date.replace(tzinfo=pytz.utc)  # Ensure it's in UTC
            create_date_local = create_date_utc.astimezone(local_tz)  # Convert to local timezone
            create_date = create_date_local.strftime('%B %d, %Y, %I:%M %p')
            print("create_date",create_date)
            videoID = False
            media_files = []
            if post.video_url:
                match = re.search(pattern, post.video_url)
                if match:
                    videoID = match.group(1)
            for img in post.image_ids:
                # Base64 encode the media content
                media_files.append({
                    'image': img,
                    'type': img.mimetype.split("/")[0],  # 'image' or 'video'
                    'mimetype': img.mimetype,  # Full MIME type (e.g., 'image/png', 'video/mp4')
                })
            
            # Add post data
            post_data.append({
                'id': post.id,
                'post_id': post,
                'message': post.message,
                'create_uid': post.create_uid.name,
                'create_date': create_date,
                'is_liked': is_liked,
                'media': media_files,  # Pass media files here
                'video_url': 'https://www.youtube.com/embed/'+str(videoID) if videoID else False,
                'comments': self.get_comments(post)
                # 'comments': [
                #     {
                #         'user': comment.create_uid.name,
                #         'message': comment.message,
                #         'date': datetime.strftime(
                #             comment.create_date.replace(tzinfo=pytz.utc).astimezone(local_tz), '%B %d, %Y, %I:%M %p'),
                #         'id': comment.id,
                #     } for comment in comments
                # ],
            })
        values = {'post_ids': post_data,'user_type':user_type, 'partner_type':partner_type}
        return http.request.render('apg_social_media.fbpostforum_customer', values)

    @http.route('/post/comment', type='json', auth='public', methods=['POST'])
    def post_comment(self, comment=False, post_id=False, parent_id=False, **kwargs):
        post_obj = request.env['apg.social.post']
        user_tz = request.env.user.tz or 'UTC'  # Get the user's timezone, default to UTC
        local_tz = pytz.timezone(user_tz)  # Convert to timezone object
        if parent_id:
            post_id = request.env['apg.post.comment'].sudo().search([('id', '=', parent_id)]).post_id.id
        if comment and post_id:
            post_id = post_obj.sudo().search([('id', '=', post_id)],limit=1)
            
            comment_details = {
                'post_id': post_id.id,
                'message': comment,
                'parent_id': parent_id if parent_id else False
            }
            comment_id = request.env['apg.post.comment'].sudo().create(comment_details)
            commant_list = []
            
            for comment in comment_id:
                create_date_utc = comment.create_date.replace(tzinfo=pytz.utc)  # Ensure it's in UTC
                create_date_local = create_date_utc.astimezone(local_tz)  # Convert to local timezone
                create_date = create_date_local.strftime('%B %d, %Y, %I:%M %p')
                commant_list.append({
                        'id': comment.id,
                        'user': comment.create_uid.name,
                        'message': comment.message,
                        'date': create_date,
                        'parent_id': comment.parent_id.id if comment.parent_id else None
                    })

            return {'success': True, 'comments': commant_list, 'message': 'Comment posted successfully'}
        return {'success': False, 'message': 'No comment provided'}

    def get_comments(self, post_id=False):
        if not post_id:
            return {'success': False, 'message': 'No post ID provided'}

        post = post_id
        comments = post.comment_ids.filtered(lambda c: not c.parent_id)  # Get only top-level comments
        return comments.get_nested_comments()
        # request.env['apg.social.post'].sudo().browse(int(post_id))
        # comments = []
        # comment_id = request.env['apg.post.comment'].sudo().search([('post_id','=',post.id)])(comment_details)
        # for comment in post.comment_ids.filtered(lambda c: not c.parent_id):
        #     replies = [{
        #         'id': reply.id,
        #         'user': reply.create_uid.name,
        #         'message': reply.message,
        #         'date': reply.create_date.strftime('%B %d, %Y, %I:%M %p'),
        #         'parent_id': reply.parent_id.id,
        #     } for reply in comment.child_ids]
        #     comments.append({
        #         'id': comment.id,
        #         'user': comment.create_uid.name,
        #         'message': comment.message,
        #         'date': comment.create_date.strftime('%B %d, %Y, %I:%M %p'),
        #         'replies': replies
        #     })
        # v
        # return comments


    @http.route('/post/like', type='json', auth='public', methods=['POST'])
    def post_like(self, post_id=False, **kwargs):
        post_obj = request.env['apg.social.post']
        if post_id:
            post_id = post_obj.sudo().search([('id', '=', post_id)],limit=1)
            like_details = {
                'post_id': post_id.id,
            }
            like_id = request.env['apg.post.like'].sudo().create(like_details)
            return {'success': True, 'like': like_id, 'message': 'Comment posted successfully'}
        return {'success': False, 'message': 'No comment provided'}

    @http.route('/post/unlike', type='json', auth='public', methods=['POST'])
    def post_unlike(self, post_id=False, **kwargs):
        like_obj = request.env['apg.post.like']
        user_id = request.env.user
        like_id = like_obj.sudo().search([('post_id', '=', int(post_id)),('create_uid', '=', user_id.id)],limit=1)
        if like_id:
            like_id.unlink()
            return {'success': True, 'message': 'Comment posted successfully'}
        return {'success': False, 'message': 'No comment provided'}

    @http.route('/post-create', type='http', auth='public', website=True)
    def post_create_creator(self, **kwargs):
        post_obj = request.env['apg.social.post']
        user_id = request.env.user.id
        """Handle file uploads."""
        # Get uploaded file
        imageUploadFile = kwargs.get('imageUploadFile')
        videoURL = kwargs.get('youtubeUrl')
        partner_type = 'creator'
        message = kwargs.get('message')
        post_id = self.post_create(post_obj,user_id,imageUploadFile,videoURL,partner_type,message)
        return request.redirect('/forumsection')

    @http.route('/post-create-partner', type='http', auth='public', website=True)
    def post_create_partner(self, **kwargs):
        post_obj = request.env['apg.social.post']
        user_id = request.env.user.id
        """Handle file uploads."""
        # Get uploaded file
        imageUploadFile = kwargs.get('imageUploadFile')
        videoURL = kwargs.get('youtubeUrl')
        partner_type = 'partner'
        message = kwargs.get('message')
        post_id = self.post_create(post_obj,user_id,imageUploadFile,videoURL,partner_type,message)
        return request.redirect('/forumsection-partner')

    def post_create(self,post_obj=False,user_id=False, imageUploadFile=False, videoURL=False, partner_type=False, message=False, **kwargs):
        post_id = False
        if imageUploadFile or message or videoURL:
            attachment_ids = []
            if imageUploadFile:
                file_content = imageUploadFile.read()
                file_name = imageUploadFile.filename
                attachment_id = request.env['ir.attachment'].sudo().create({
                    'name': file_name,
                    'type': 'binary',
                    'datas': base64.b64encode(file_content),
                    'res_model': 'apg.social.post',  # Replace with the model you want to attach to
                    # 'res_id': user_id,  # Replace with the record ID
                })
                attachment_ids.append(attachment_id.id)
            post_id = post_obj.sudo().create({
                'partner_type': partner_type,
                'image_ids': [(6, 0, attachment_ids)] if attachment_ids else False,
                'video_url': videoURL,
                'message': message,
                })
        return post_id
