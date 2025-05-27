from typing import List

from hmcplugins.cross_case import case_images
from hmcplugins.general import file_mime_class, browser_history_count, browser_history_category, calendar, contacts, \
    emails, file_categories, file_extensions, file_mime_types, financial_traces, general_info, locations, trace_types, \
    os_present
from hmcplugins.phone import application_category, application_count, application_presence, calls, chat_counts, \
    chat_application_counts, text_input, notes, social_media, accounts, os_info_ufed, life_time_info_ufed
from hmcplugins.windows import win_application_count, win_life_time, win_application_presence, win_version, \
    win_prefetch_count, win_lnk_count, win_event_log_count

plugin_registry = {
    # cross-case
    "case_images": case_images.CaseImages,
    # general
    "browser_history_count": browser_history_count.BrowserHistoryCount,
    "browser_history_category": browser_history_category.BrowserHistoryCategory,
    "calendar": calendar.Calendar,
    "contacts": contacts.Contacts,
    "emails": emails.Emails,
    "file_categories": file_categories.FileCategories,
    "file_extensions": file_extensions.FileExtensions,
    "file_mime_class": file_mime_class.MimeClasses,
    "file_mime_types": file_mime_types.MimeTypes,
    "financial_traces": financial_traces.FinancialTraces,
    "general_info": general_info.General,
    "locations": locations.Locations,
    "trace_types": trace_types.TraceTypes,
    "os_present": os_present.OSPresent,
    #phone
    "application_category": application_category.ApplicationCategory,
    "application_count": application_count.ApplicationCount,
    "application_presence": application_presence.ApplicationPresence,
    "calls": calls.PhoneCalls,
    "chat_counts": chat_counts.ChatCounts,
    "chat_application_counts": chat_application_counts.ChatApplicationCounts,
    "notes": notes.Notes,
    "text_input": text_input.TextInput,
    "social_media": social_media.SocialMedia,
    "accounts": accounts.Accounts,
    "os_info_ufed": os_info_ufed.OSInfoUfed,
    "life_time_info_ufed": life_time_info_ufed.LifeTimeInfoUfed,
    #windows
    "win_application_count": win_application_count.WinApplicationCount,
    "win_application_presence": win_application_presence.WinApplicationPresence,
    "win_life_time": win_life_time.WinLifeTime,
    "win_version": win_version.WinVersion,
    "win_prefetch_count": win_prefetch_count.WinPrefetchCount,
    "win_lnk_count": win_lnk_count.WinLnkCount,
    "win_event_log_count": win_event_log_count.WinEventLogCount,
}

def load_enabled_plugins(enabled_plugins: List[str]):
    plugins = []

    for name in enabled_plugins:
        plugin_class = plugin_registry.get(name)
        if plugin_class:
            plugins.append(plugin_class())
        else:
            print(f"Plugin not found in registry: {name} \nSkipping...")

    return plugins