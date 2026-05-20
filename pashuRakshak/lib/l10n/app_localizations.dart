import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/intl.dart' as intl;

import 'app_localizations_en.dart';
import 'app_localizations_hi.dart';
import 'app_localizations_mr.dart';

// ignore_for_file: type=lint

/// Callers can lookup localized strings with an instance of AppLocalizations
/// returned by `AppLocalizations.of(context)`.
///
/// Applications need to include `AppLocalizations.delegate()` in their app's
/// `localizationDelegates` list, and the locales they support in the app's
/// `supportedLocales` list. For example:
///
/// ```dart
/// import 'l10n/app_localizations.dart';
///
/// return MaterialApp(
///   localizationsDelegates: AppLocalizations.localizationsDelegates,
///   supportedLocales: AppLocalizations.supportedLocales,
///   home: MyApplicationHome(),
/// );
/// ```
///
/// ## Update pubspec.yaml
///
/// Please make sure to update your pubspec.yaml to include the following
/// packages:
///
/// ```yaml
/// dependencies:
///   # Internationalization support.
///   flutter_localizations:
///     sdk: flutter
///   intl: any # Use the pinned version from flutter_localizations
///
///   # Rest of dependencies
/// ```
///
/// ## iOS Applications
///
/// iOS applications define key application metadata, including supported
/// locales, in an Info.plist file that is built into the application bundle.
/// To configure the locales supported by your app, you’ll need to edit this
/// file.
///
/// First, open your project’s ios/Runner.xcworkspace Xcode workspace file.
/// Then, in the Project Navigator, open the Info.plist file under the Runner
/// project’s Runner folder.
///
/// Next, select the Information Property List item, select Add Item from the
/// Editor menu, then select Localizations from the pop-up menu.
///
/// Select and expand the newly-created Localizations item then, for each
/// locale your application supports, add a new item and select the locale
/// you wish to add from the pop-up menu in the Value field. This list should
/// be consistent with the languages listed in the AppLocalizations.supportedLocales
/// property.
abstract class AppLocalizations {
  AppLocalizations(String locale)
    : localeName = intl.Intl.canonicalizedLocale(locale.toString());

  final String localeName;

  static AppLocalizations? of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations);
  }

  static const LocalizationsDelegate<AppLocalizations> delegate =
      _AppLocalizationsDelegate();

  /// A list of this localizations delegate along with the default localizations
  /// delegates.
  ///
  /// Returns a list of localizations delegates containing this delegate along with
  /// GlobalMaterialLocalizations.delegate, GlobalCupertinoLocalizations.delegate,
  /// and GlobalWidgetsLocalizations.delegate.
  ///
  /// Additional delegates can be added by appending to this list in
  /// MaterialApp. This list does not have to be used at all if a custom list
  /// of delegates is preferred or required.
  static const List<LocalizationsDelegate<dynamic>> localizationsDelegates =
      <LocalizationsDelegate<dynamic>>[
        delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
      ];

  /// A list of this localizations delegate's supported locales.
  static const List<Locale> supportedLocales = <Locale>[
    Locale('en'),
    Locale('hi'),
    Locale('mr'),
  ];

  /// Application title
  ///
  /// In en, this message translates to:
  /// **'PashuRakshak'**
  String get appTitle;

  /// Language selection prompt
  ///
  /// In en, this message translates to:
  /// **'Select Language'**
  String get selectLanguage;

  /// Login button text
  ///
  /// In en, this message translates to:
  /// **'Login'**
  String get login;

  /// Register button text
  ///
  /// In en, this message translates to:
  /// **'Register'**
  String get register;

  /// Mobile number field label
  ///
  /// In en, this message translates to:
  /// **'Mobile Number'**
  String get mobileNumber;

  /// Password field label
  ///
  /// In en, this message translates to:
  /// **'Password'**
  String get password;

  /// Confirm password field label
  ///
  /// In en, this message translates to:
  /// **'Confirm Password'**
  String get confirmPassword;

  /// Submit button text
  ///
  /// In en, this message translates to:
  /// **'Submit'**
  String get submit;

  /// Cancel button text
  ///
  /// In en, this message translates to:
  /// **'Cancel'**
  String get cancel;

  /// Schemes tab label
  ///
  /// In en, this message translates to:
  /// **'Schemes'**
  String get schemes;

  /// Applications tab label
  ///
  /// In en, this message translates to:
  /// **'My Applications'**
  String get myApplications;

  /// Notifications tab label
  ///
  /// In en, this message translates to:
  /// **'Notifications'**
  String get notifications;

  /// Profile tab label
  ///
  /// In en, this message translates to:
  /// **'Profile'**
  String get profile;

  /// Settings label
  ///
  /// In en, this message translates to:
  /// **'Settings'**
  String get settings;

  /// Home tab label
  ///
  /// In en, this message translates to:
  /// **'Home'**
  String get home;

  /// Scheme name label
  ///
  /// In en, this message translates to:
  /// **'Scheme Name'**
  String get schemeName;

  /// Scheme details title
  ///
  /// In en, this message translates to:
  /// **'Scheme Details'**
  String get schemeDetails;

  /// Know more button text
  ///
  /// In en, this message translates to:
  /// **'Know More'**
  String get knowMore;

  /// Apply now button text
  ///
  /// In en, this message translates to:
  /// **'Apply Now'**
  String get applyNow;

  /// Register for scheme title
  ///
  /// In en, this message translates to:
  /// **'Register for Scheme'**
  String get registerForScheme;

  /// Farmer name field label
  ///
  /// In en, this message translates to:
  /// **'Farmer Name'**
  String get farmerName;

  /// Date of birth field label
  ///
  /// In en, this message translates to:
  /// **'Date of Birth'**
  String get dateOfBirth;

  /// State field label
  ///
  /// In en, this message translates to:
  /// **'State'**
  String get state;

  /// District field label
  ///
  /// In en, this message translates to:
  /// **'District'**
  String get district;

  /// Acres of land field label
  ///
  /// In en, this message translates to:
  /// **'Acres of Land'**
  String get acresOfLand;

  /// Cattle count field label
  ///
  /// In en, this message translates to:
  /// **'Cattle Count'**
  String get cattleCount;

  /// Upload Aadhaar document
  ///
  /// In en, this message translates to:
  /// **'Upload Aadhaar'**
  String get uploadAadhaar;

  /// Upload 7/12 extract document
  ///
  /// In en, this message translates to:
  /// **'Upload 7/12 Extract'**
  String get upload712;

  /// Upload farmer proof document
  ///
  /// In en, this message translates to:
  /// **'Upload Farmer Proof'**
  String get uploadFarmerProof;

  /// Upload cattle images
  ///
  /// In en, this message translates to:
  /// **'Upload Cattle Images'**
  String get uploadCattleImages;

  /// Upload cattle videos
  ///
  /// In en, this message translates to:
  /// **'Upload Cattle Videos'**
  String get uploadCattleVideos;

  /// Step 1 title
  ///
  /// In en, this message translates to:
  /// **'Basic Details'**
  String get step1BasicDetails;

  /// Step 2 title
  ///
  /// In en, this message translates to:
  /// **'Documents'**
  String get step2Documents;

  /// Step 3 title
  ///
  /// In en, this message translates to:
  /// **'Cattle Proof'**
  String get step3CattleProof;

  /// Next button text
  ///
  /// In en, this message translates to:
  /// **'Next'**
  String get next;

  /// Previous button text
  ///
  /// In en, this message translates to:
  /// **'Previous'**
  String get previous;

  /// Approved status
  ///
  /// In en, this message translates to:
  /// **'Approved'**
  String get approved;

  /// Rejected status
  ///
  /// In en, this message translates to:
  /// **'Rejected'**
  String get rejected;

  /// Pending status
  ///
  /// In en, this message translates to:
  /// **'Pending'**
  String get pending;

  /// Under review status
  ///
  /// In en, this message translates to:
  /// **'Under Review'**
  String get underReview;

  /// Validation history title
  ///
  /// In en, this message translates to:
  /// **'Validation History'**
  String get validationHistory;

  /// Download report button
  ///
  /// In en, this message translates to:
  /// **'Download Report'**
  String get downloadReport;

  /// Application status title
  ///
  /// In en, this message translates to:
  /// **'Application Status'**
  String get applicationStatus;

  /// Change language setting
  ///
  /// In en, this message translates to:
  /// **'Change Language'**
  String get changeLanguage;

  /// Dark mode toggle
  ///
  /// In en, this message translates to:
  /// **'Dark Mode'**
  String get darkMode;

  /// About section
  ///
  /// In en, this message translates to:
  /// **'About'**
  String get about;

  /// Support section
  ///
  /// In en, this message translates to:
  /// **'Support'**
  String get support;

  /// Logout button
  ///
  /// In en, this message translates to:
  /// **'Logout'**
  String get logout;

  /// English language option
  ///
  /// In en, this message translates to:
  /// **'English'**
  String get english;

  /// Hindi language option
  ///
  /// In en, this message translates to:
  /// **'हिन्दी'**
  String get hindi;

  /// Marathi language option
  ///
  /// In en, this message translates to:
  /// **'मराठी'**
  String get marathi;

  /// Welcome back greeting
  ///
  /// In en, this message translates to:
  /// **'Welcome Back'**
  String get welcomeBack;

  /// Active schemes section title
  ///
  /// In en, this message translates to:
  /// **'Active Schemes'**
  String get activeSchemes;

  /// Empty state for schemes
  ///
  /// In en, this message translates to:
  /// **'No schemes available'**
  String get noSchemesAvailable;

  /// Empty state for applications
  ///
  /// In en, this message translates to:
  /// **'No applications yet'**
  String get noApplications;

  /// Empty state for notifications
  ///
  /// In en, this message translates to:
  /// **'No notifications'**
  String get noNotifications;

  /// Full name field label
  ///
  /// In en, this message translates to:
  /// **'Full Name'**
  String get fullName;

  /// Email field label
  ///
  /// In en, this message translates to:
  /// **'Email'**
  String get email;

  /// Address field label
  ///
  /// In en, this message translates to:
  /// **'Address'**
  String get address;

  /// Signup prompt
  ///
  /// In en, this message translates to:
  /// **'Don\'t have an account?'**
  String get dontHaveAccount;

  /// Login prompt
  ///
  /// In en, this message translates to:
  /// **'Already have an account?'**
  String get alreadyHaveAccount;

  /// Create account title
  ///
  /// In en, this message translates to:
  /// **'Create Account'**
  String get createAccount;

  /// Quick stats section title
  ///
  /// In en, this message translates to:
  /// **'Quick Stats'**
  String get quickStats;

  /// Total applications stat
  ///
  /// In en, this message translates to:
  /// **'Total Applications'**
  String get totalApplications;

  /// Approved applications stat
  ///
  /// In en, this message translates to:
  /// **'Approved'**
  String get approvedApplications;

  /// Pending applications stat
  ///
  /// In en, this message translates to:
  /// **'Pending'**
  String get pendingApplications;

  /// Rejected applications stat
  ///
  /// In en, this message translates to:
  /// **'Rejected'**
  String get rejectedApplications;

  /// Edit profile button
  ///
  /// In en, this message translates to:
  /// **'Edit Profile'**
  String get editProfile;

  /// Save changes button
  ///
  /// In en, this message translates to:
  /// **'Save Changes'**
  String get saveChanges;

  /// Application ID label
  ///
  /// In en, this message translates to:
  /// **'Application ID'**
  String get applicationId;

  /// Applied on date label
  ///
  /// In en, this message translates to:
  /// **'Applied On'**
  String get appliedOn;

  /// Last updated date label
  ///
  /// In en, this message translates to:
  /// **'Last Updated'**
  String get lastUpdated;

  /// Scheme amount label
  ///
  /// In en, this message translates to:
  /// **'Scheme Amount'**
  String get schemeAmount;

  /// Eligibility label
  ///
  /// In en, this message translates to:
  /// **'Eligibility'**
  String get eligibility;

  /// Deadline label
  ///
  /// In en, this message translates to:
  /// **'Deadline'**
  String get deadline;

  /// Description label
  ///
  /// In en, this message translates to:
  /// **'Description'**
  String get description;

  /// Documents label
  ///
  /// In en, this message translates to:
  /// **'Documents'**
  String get documents;

  /// Village field label
  ///
  /// In en, this message translates to:
  /// **'Village'**
  String get village;

  /// Pincode field label
  ///
  /// In en, this message translates to:
  /// **'Pincode'**
  String get pincode;

  /// Gender field label
  ///
  /// In en, this message translates to:
  /// **'Gender'**
  String get gender;

  /// Male option
  ///
  /// In en, this message translates to:
  /// **'Male'**
  String get male;

  /// Female option
  ///
  /// In en, this message translates to:
  /// **'Female'**
  String get female;

  /// Other option
  ///
  /// In en, this message translates to:
  /// **'Other'**
  String get other;

  /// Upload mobile bill label
  ///
  /// In en, this message translates to:
  /// **'Upload Mobile Bill'**
  String get uploadMobileBill;

  /// Cattle type field label
  ///
  /// In en, this message translates to:
  /// **'Cattle Type'**
  String get cattleType;

  /// Upload proof images label
  ///
  /// In en, this message translates to:
  /// **'Upload Proof Images'**
  String get uploadProofImages;

  /// Government of India text
  ///
  /// In en, this message translates to:
  /// **'Government of India'**
  String get govtOfIndia;

  /// Ministry name
  ///
  /// In en, this message translates to:
  /// **'Ministry of Agriculture & Farmers Welfare'**
  String get ministryOfAgriculture;

  /// App subtitle
  ///
  /// In en, this message translates to:
  /// **'Smart Livestock Verification & Grant Monitoring'**
  String get smartLivestock;

  /// Login prompt
  ///
  /// In en, this message translates to:
  /// **'Login to continue'**
  String get loginToContinue;

  /// Mobile field hint
  ///
  /// In en, this message translates to:
  /// **'Enter your mobile number'**
  String get enterMobileNumber;

  /// Password field hint
  ///
  /// In en, this message translates to:
  /// **'Enter your password'**
  String get enterPassword;

  /// Required field validation
  ///
  /// In en, this message translates to:
  /// **'This field is required'**
  String get fieldRequired;

  /// Invalid mobile validation
  ///
  /// In en, this message translates to:
  /// **'Enter a valid 10-digit mobile number'**
  String get invalidMobile;

  /// Short password validation
  ///
  /// In en, this message translates to:
  /// **'Password must be at least 6 characters'**
  String get passwordTooShort;

  /// Version label
  ///
  /// In en, this message translates to:
  /// **'Version'**
  String get version;

  /// App description for about page
  ///
  /// In en, this message translates to:
  /// **'PashuRakshak is a smart livestock verification and government grant monitoring system designed to help farmers access government schemes efficiently.'**
  String get appDescription;
}

class _AppLocalizationsDelegate
    extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  Future<AppLocalizations> load(Locale locale) {
    return SynchronousFuture<AppLocalizations>(lookupAppLocalizations(locale));
  }

  @override
  bool isSupported(Locale locale) =>
      <String>['en', 'hi', 'mr'].contains(locale.languageCode);

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}

AppLocalizations lookupAppLocalizations(Locale locale) {
  // Lookup logic when only language code is specified.
  switch (locale.languageCode) {
    case 'en':
      return AppLocalizationsEn();
    case 'hi':
      return AppLocalizationsHi();
    case 'mr':
      return AppLocalizationsMr();
  }

  throw FlutterError(
    'AppLocalizations.delegate failed to load unsupported locale "$locale". This is likely '
    'an issue with the localizations generation tool. Please file an issue '
    'on GitHub with a reproducible sample app and the gen-l10n configuration '
    'that was used.',
  );
}
