from django.db import models

# Create your models here.
LANGUAGE_CHOICE = (
    ("ru", "Русский"),
    ("en", "Английский"),
    ("es", "Испанский"),
    ("ar", "Арабский"),
    ("hi", "Хинди"),
    ("pt", "Португальский"),
    ("zh", "Китайский"),
    ("ja", "Японский"),
)


class DataForApp(models.Model):
    language = models.CharField(
        max_length=20, choices=LANGUAGE_CHOICE, blank=True, null=True
    )
    auth_sign_in_email = models.CharField(max_length=1000, blank=True, null=True)
    auth_sign_in_password = models.CharField(max_length=1000, blank=True, null=True)
    auth_sign_in_login = models.CharField(max_length=1000, blank=True, null=True)
    auth_sign_up = models.CharField(max_length=1000, blank=True, null=True)
    auth_sign_in_join= models.CharField(max_length=1000, blank=True, null=True)
    auth_sign_up_nickname= models.CharField(max_length=1000, blank=True, null=True)
    auth_sign_up_phone= models.CharField(max_length=1000, blank=True, null=True)
    auth_sign_up_time_choice= models.CharField(max_length=1000, blank=True, null=True)
    auth_sign_up_time_ten= models.CharField(max_length=1000, blank=True, null=True)
    auth_sign_up_avatar_text= models.CharField(max_length=1000, blank=True, null=True)
    auth_sign_up_add_avatar= models.CharField(max_length=1000, blank=True, null=True)
    auth_sign_up_continue_button= models.CharField(max_length=1000, blank=True, null=True)
    intro_swipe_text= models.CharField(max_length=1000, blank=True, null=True)
    intro_text_one= models.CharField(max_length=1000, blank=True, null=True)
    intro_text_two= models.CharField(max_length=1000, blank=True, null=True)
    intro_text_three= models.CharField(max_length=1000, blank=True, null=True)
    intro_text_four = models.CharField(max_length=1000, blank=True, null=True)
    intro_text_five = models.CharField(max_length=1000, blank=True, null=True)
    intro_text_six = models.CharField(max_length=1000, blank=True, null=True)
    intro_text_seven = models.CharField(max_length=1000, blank=True, null=True)
    intro_text_eight = models.CharField(max_length=1000, blank=True, null=True)
    intro_text_nine = models.CharField(max_length=1000, blank=True, null=True)
    intro_text_ten = models.CharField(max_length=1000, blank=True, null=True)
    intro_text_ten_first = models.CharField(max_length=1000, blank=True, null=True)
    intro_text_ten_second = models.CharField(max_length=1000, blank=True, null=True)
    intro_text_ten_third = models.CharField(max_length=1000, blank=True, null=True)
    intro_text_eleven = models.CharField(max_length=1000, blank=True, null=True)
    intro_text_twelve = models.CharField(max_length=1000, blank=True, null=True)
    dropdown_menu_change_avatar = models.CharField(
        max_length=1000, blank=True, null=True
    )
    dropdown_menu_change_nickname = models.CharField(
        max_length=1000, blank=True, null=True
    )
    dropdown_menu_invite_link = models.CharField(max_length=1000, blank=True, null=True)
    dropdown_menu_faq = models.CharField(max_length=1000, blank=True, null=True)
    dropdown_menu_wallet = models.CharField(max_length=1000, blank=True, null=True)
    dropdown_menu_roadmap= models.CharField(max_length=1000, blank=True, null=True)
    dropdown_menu_integration= models.CharField(max_length=1000, blank=True, null=True)
    dropdown_menu_privacy_button = models.CharField(max_length=1000, blank=True, null=True)
    dropdown_menu_terms_button= models.CharField(max_length=1000, blank=True, null=True)
    dropdown_menu_logout_button= models.CharField(max_length=1000, blank=True, null=True)
    calendar_schedule_new_practice= models.CharField(max_length=1000, blank=True, null=True)
    calendar_schedule_date_time= models.CharField(max_length=1000, blank=True, null=True)
    calendar_schedule_invite_link = models.CharField(max_length=1000, blank=True, null=True)
    calendar_schedule_scheduled_practice = models.CharField(max_length=1000, blank=True, null=True)
    calendar_schedule_copy_link= models.CharField(max_length=1000, blank=True, null=True)
    calendar_schedule_past_practice= models.CharField(max_length=1000, blank=True, null=True)
    calendar_schedule_past= models.CharField(max_length=1000, blank=True, null=True)
    finance_available_balance = models.CharField(max_length=1000, blank=True, null=True)
    finance_locked_tokens = models.CharField(max_length=1000, blank=True, null=True)
    finance_unlocked_value = models.CharField(max_length=1000, blank=True, null=True)
    finance_tokens_progress_text = models.CharField(max_length=1000, blank=True, null=True)
    finance_tokens_development_text = models.CharField(max_length=1000, blank=True, null=True)
    finance_send_omt= models.CharField(max_length=1000, blank=True, null=True)
    finance_buy_omt= models.CharField(max_length=1000, blank=True, null=True)
    user_page_time_practice = models.CharField(max_length=1000, blank=True, null=True)
    user_page_daily_practice = models.CharField(max_length=1000, blank=True, null=True)
    user_page_continuous_practice = models.CharField(
        max_length=1000, blank=True, null=True
    )
    user_page_progress_booster = models.CharField(
        max_length=1000, blank=True, null=True
    )
    user_page_luminaries_involved = models.CharField(
        max_length=1000, blank=True, null=True
    )
    user_page_group_practice_button = models.CharField(
        max_length=1000, blank=True, null=True
    )
    user_page_start_practice_button = models.CharField(
        max_length=1000, blank=True, null=True
    )
    user_page_wish_chat_button = models.CharField(
        max_length=1000, blank=True, null=True
    )
    user_page_time_minute = models.CharField(max_length=1000, blank=True, null=True)
    user_page_time_second = models.CharField(max_length=1000, blank=True, null=True)
    user_page_time_day= models.CharField(max_length=1000, blank=True, null=True)
    meditation_onboarding_text_one = models.CharField(max_length=1000, blank=True, null=True)
    meditation_onboarding_text_two = models.CharField(max_length=1000, blank=True, null=True)
    meditation_onboarding_text_three = models.CharField(max_length=1000, blank=True, null=True)
    meditation_onboarding_in_meditation = models.CharField(max_length=1000, blank=True, null=True)
    meditation_onboarding_finish_process = models.CharField(max_length=1000, blank=True, null=True)
    meditation_onboarding_continuous_time = models.CharField(max_length=1000, blank=True, null=True)
    meditation_onboarding_team_practice = models.CharField(max_length=1000, blank=True, null=True)
    meditation_onboarding_thanks_button = models.CharField(max_length=1000, blank=True, null=True)
    meditation_onboarding_lightning_wishes= models.CharField(max_length=1000, blank=True, null=True)
    auth_sign_phone = models.CharField(max_length=1000, blank=True, null=True)
    auth_sign_email = models.CharField(max_length=1000, blank=True, null=True)
    auth_sign_password= models.CharField(max_length=1000, blank=True, null=True)
    profile_delete_acc= models.CharField(max_length=1000, blank=True, null=True)
    profile_delete_info= models.CharField(max_length=1000, blank=True, null=True)
    profile_delete_info_yes= models.CharField(max_length=1000, blank=True, null=True)
    profile_delete_info_no= models.CharField(max_length=1000, blank=True, null=True)
    forgot_password_button= models.CharField(max_length=1000, blank=True, null=True)
    error_email_not_registered= models.CharField(max_length=1000, blank=True, null=True)
    error_email_wrong_code= models.CharField(max_length=1000, blank=True, null=True)
    password_success_changed= models.CharField(max_length=1000, blank=True, null=True)
    error_happened= models.CharField(max_length=1000, blank=True, null=True)
    error_image_upload_failed= models.CharField(max_length=1000, blank=True, null=True)
    error_image_failed= models.CharField(max_length=1000, blank=True, null=True)
    email_link_sent= models.CharField(max_length=1000, blank=True, null=True)
    email_link_code= models.CharField(max_length=1000, blank=True, null=True)
    code_from_sms= models.CharField(max_length=1000, blank=True, null=True)
    change_password_account= models.CharField(max_length=1000, blank=True, null=True)
    change_confirm_button = models.CharField(max_length=1000, blank=True, null=True)
    change_send_code = models.CharField(max_length=1000, blank=True, null=True)
    error_email_format = models.CharField(max_length=1000, blank=True, null=True)
    error_sent_code = models.CharField(max_length=1000, blank=True, null=True)
    change_password_by_own = models.CharField(max_length=1000, blank=True, null=True)
    enter_sent_code = models.CharField(max_length=1000, blank=True, null=True)
    button_ready = models.CharField(max_length=1000, blank=True, null=True)
    error_password_characters = models.CharField(max_length=1000, blank=True, null=True)
    error_incorrect_sms = models.CharField(max_length=1000, blank=True, null=True)
    error_email_already_used = models.CharField(max_length=1000, blank=True, null=True)
    error_number_already_used = models.CharField(max_length=1000, blank=True, null=True)
    error_incorrect_number= models.CharField(max_length=1000, blank=True, null=True)
    error_enter_correct_number = models.CharField(max_length=1000, blank=True, null=True)
    error_enter_correct_email= models.CharField(max_length=1000, blank=True, null=True)
    error_deleting_account = models.CharField(max_length=1000, blank=True, null=True)
    success_deleting_account = models.CharField(max_length=1000, blank=True, null=True)
    success_image_changed = models.CharField(max_length=1000, blank=True, null=True)
    success_nickname_saved = models.CharField(max_length=1000, blank=True, null=True)
    error_nickname_empty = models.CharField(max_length=1000, blank=True, null=True)
    error_unknown = models.CharField(max_length=1000, blank=True, null=True)
    error_email_already = models.CharField(max_length=1000, blank=True, null=True)
    error_phone_already = models.CharField(max_length=1000, blank=True, null=True)
    error_try_again = models.CharField(max_length=1000, blank=True, null=True)
    error_failed_onboarding_content = models.CharField(
        max_length=1000, blank=True, null=True
    )
    hint_text_type_here = models.CharField(max_length=1000, blank=True, null=True)
    number_in_meditation = models.CharField(max_length=1000, blank=True, null=True)
    button_complete = models.CharField(max_length=1000, blank=True, null=True)
    error_phone_empty= models.CharField(max_length=1000, blank=True, null=True)
    error_password_required= models.CharField(max_length=1000, blank=True, null=True)
    error_password_length= models.CharField(max_length=1000, blank=True, null=True)
    error_password_uppercase= models.CharField(max_length=1000, blank=True, null=True)
    error_password_digit= models.CharField(max_length=1000, blank=True, null=True)
    message_type= models.CharField(max_length=1000, blank=True, null=True)
    user_not_exist= models.CharField(max_length=1000, blank=True, null=True)
    select_sign_up= models.CharField(max_length=1000, blank=True, null=True)
    invalid_combination_of_credentials= models.CharField(max_length=1000, blank=True, null=True)
    grant_access_to_photos= models.CharField(max_length=1000, blank=True, null=True)
    sign_in_google= models.CharField(max_length=1000, blank=True, null=True)
    sign_in_apple= models.CharField(max_length=1000, blank=True, null=True)
    sign_in_no_acc = models.CharField(max_length=1000, blank=True, null=True)
    sign_in_or= models.CharField(max_length=1000, blank=True, null=True)
    error_sign_apple= models.CharField(max_length=1000, blank=True, null=True)
    error_sign_google  = models.CharField(max_length=1000, blank=True, null=True)
    error_load_locaization   = models.CharField(max_length=1000, blank=True, null=True)
    error_initalization_videoplayer = models.CharField(max_length=1000, blank=True, null=True)
    server_error= models.CharField(max_length=1000, blank=True, null=True)
    sign_create_account  = models.CharField(max_length=1000, blank=True, null=True)
    sign_your_email  = models.CharField(max_length=1000, blank=True, null=True)
    sign_your_password= models.CharField(max_length=1000, blank=True, null=True)
    save_account_info= models.CharField(max_length=1000, blank=True, null=True)
    enter_correct_email= models.CharField(max_length=1000, blank=True, null=True)
    sign_type_login= models.CharField(max_length=1000, blank=True, null=True)
    error_occurred= models.CharField(max_length=1000, blank=True, null=True)
    progress_booster_x = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        verbose_name = "Перевод"
        verbose_name_plural = "Перевод"
