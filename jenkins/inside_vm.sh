#!/bin/bash

function title(){ CHAR='*';CONTENT="$CHAR $* $CHAR";BORDER=$(echo "$CONTENT" | sed "s/./$CHAR/g");echo "";echo "$BORDER";echo "$CONTENT";echo "$BORDER";}
function subtitle(){ CHAR=' ';CONTENT="$CHAR $* $CHAR";BORDER=$(echo "$CONTENT" | sed "s/./$CHAR/g");echo "";echo "$BORDER";echo "$CONTENT";echo "$BORDER";}

function activate_environment {
    echo "Activated environment"
}

function start_postgres {
    # Switch to postgres (and start it)
    ./manage.py postgres start
    ./manage.py migrate --noinput
}

function stop_postgres {
    # Clean up our database
    ./manage.py postgres stop
}

function selenium_tests {
    # Run live tests
    subtitle "TESTING_END_TO_END FIREFOX"
    firefox --version
    WebDriver=gecko timeout -k 10m 9m ./runlivetests.sh
    LIVETEST_CHECK1=$?

    subtitle "TESTING_END_TO_END CHROMIUM"
    chromium --version
    WebDriver=chrome timeout -k 10m 9m ./runlivetests.sh
    LIVETEST_CHECK2=$?
}

function unit_tests {
    # Run tests and coverage
    subtitle "TESTING"
    echo "TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'" > boligadmin/settings/auto/test_runner.py
    echo "TEST_OUTPUT_DIR = os.path.join(BASE_DIR, '../reports/test/')" >> boligadmin/settings/auto/test_runner.py
    ./runtests.sh
    TEST_CHECK=$?
    coverage report
    mkdir -p ../reports/
    coverage xml -o ../reports/coverage.xml
    mkdir -p ../reports/coverage_html/
    coverage html -d ../reports/coverage_html/
}

function integration_tests {
    # Run healthcheck / system integration tests
    subtitle "PULLING DOCKER IMAGES"
    grep "image = " -r core/management/commands/*.py | sed "s/.* = '\(.*\)'/\1/g" | xargs -l1 docker pull

    subtitle "TESTING_SYSTEM_INTEGRATION"
    timeout -k 20m 15m ./runhealthtests.py
    HEALTHTEST_CHECK=$?
}

function translation_checking {
    # Compile messages and check that everything is translated
    subtitle "CHECKING TRANSLATION"
    ./compile_messages.sh
    COMPILE_MESSAGES_CHECK=$?

    ./find_missing_i18n.sh
    MISSING_I18N_CHECK=$?

    ./find_missing_translations.sh
    TRANSLATE_CHECK=$?

    subtitle "CHECKING DIFF"
    DIFF=$(git diff --raw | grep -v "vagrant" | grep -v "boligadmin/settings" | grep -v "adminapp/frontend/res.xml")
    if [ -z "$DIFF" ]; then
        DIFF_CHECK=0
    else
        echo "$DIFF"
        DIFF_CHECK=1
    fi

    subtitle "CHECKING LICENCE MAPPING"
    ./licence/check_mapping.py
    MAPPING_CHECK=$?
}

function code_checking {
    # Check code style
    subtitle "CHECKING CODE"
    mkdir -p ../reports/

    I18NLINT_TEMPLATE=$(./i18nlint_templates.sh)
    I18NLINT_TEMPLATE_CHECK=$?
    echo "$I18NLINT_TEMPLATE" | sed "s#\./##g" | tee ../reports/i18nlint_templates.log

    LINT=$(./lint.sh -f parseable)
    LINT_CHECK=$?
    echo "$LINT" | tee ../reports/lint.log

    LINT_TESTS=$(./lint_tests.sh -f parseable)
    LINT_TESTS_CHECK=$?
    echo "$LINT_TESTS" | tee ../reports/lint_tests.log

    PEP8=$(./pycodestyle.sh)
    PEP8_CHECK=$?
    echo "$PEP8" | sed "s#\./##g" | tee ../reports/pycodestyle.log

    # Concatenate test results
    cat ../reports/i18nlint_templates.log ../reports/pycodestyle.log > ../reports/pep8.log
    cat ../reports/lint.log ../reports/lint_tests.log > ../reports/pylint.log

    subtitle "CHECKING DATAMODEL"
    ./tools/reverse_model_checker.sh webapp/models/
    REVERSE_WEBAPP_CHECK=$?
    echo ""

    ./tools/reverse_model_checker.sh adminapp/models/
    REVERSE_ADMINAPP_CHECK=$?
    echo ""
}

function docs_generation {
    # Generate documentation
    subtitle "GENERATING DOCS"
    ./build_documentation.sh
    DOCUMENTATION_CHECK=$?
    mkdir -p ../reports/docs/
    cp -r docs/_build/html/ ../reports/docs/
}

function database_checking {
    ./tools/makemigrations_needed.sh
    MIGRATIONS_CHECK=$?
    echo ""
}

# Print out all failing tests
EXIT_STATUS=0
function test_and_fail {
    var=$1
    msg=$2
    STATUS=${!var} 
    EXIT_STATUS=$(($EXIT_STATUS || $STATUS))
    if [ $STATUS -ne 0 ]; then
        echo "$var - $msg"
    fi
}


if [ "$TASK" == "End-to-End Tests" ]; then
    title "Executing task: $TASK"
    # Setup
    activate_environment
    # start_postgres
    # Content
    selenium_tests
    # Error reporting
    title "Failing tests:"
    test_and_fail LIVETEST_CHECK1 "One or more selenium test-cases failed (gecko)."
    test_and_fail LIVETEST_CHECK2 "One or more selenium test-cases failed (chrome)."
    # Shutdown
    # stop_postgres
elif [ "$TASK" == "Documentation" ]; then
    title "Executing task: $TASK"
    # Setup
    activate_environment
    # Content
    docs_generation
    # Error reporting
    test_and_fail DOCUMENTATION_CHECK "Documentation generator throws errors."
    # Shutdown (empty)
elif [ "$TASK" == "Checking" ]; then
    title "Executing task: $TASK"
    # Setup
    activate_environment
    # Content
    translation_checking
    code_checking
    database_checking
     # Error reporting
    test_and_fail COMPILE_MESSAGES_CHECK "Compiling locales failed."
    test_and_fail MISSING_I18N_CHECK "Some files were missing i18n includes."
    test_and_fail TRANSLATE_CHECK "Translations were missing or fuzzy."
    test_and_fail LINT_CHECK "The pylinter found issues with the code (python)."
    test_and_fail I18NLINT_TEMPLATE_CHECK "The pylinter found translation issues with the code (html)."
    test_and_fail LINT_TESTS_CHECK "The pylinter found issues with the test code (python)."
    test_and_fail PEP8_CHECK "Code did not pass PEP8 checks."
    test_and_fail REVERSE_WEBAPP_CHECK "Missing reverse comments in webapp."
    test_and_fail REVERSE_ADMINAPP_CHECK "Missing reverse comments in adminapp."
    test_and_fail MIGRATIONS_CHECK "Needs to run makemigrations."
    test_and_fail DIFF_CHECK "Checking the code, changed the code."
    test_and_fail MAPPING_CHECK "The requirements and licence files were not in sync."
    # Shutdown (empty)
elif [ "$TASK" == "UBS" ]; then
    title "Executing task: $TASK"
    # Setup
    activate_environment
    # start_postgres
    # Content
    unit_tests
    # Error reporting
    test_and_fail TEST_CHECK "One or more unittest-cases failed."
    # Shutdown
    # stop_postgres
elif [ "$TASK" == "Integration Tests" ]; then
    title "Executing task: $TASK"
    # Setup
    activate_environment
    # start_postgres
    # Content
    integration_tests
    subtitle "Testing populate_db.py"
    ./tools/test_gen_data.sh
    # Error reporting
    test_and_fail HEALTHTEST_CHECK "One or more system integration test-cases failed."
    # Shutdown
    # stop_postgres
else
    echo "Unknown TASK: $TASK"
    EXIT_STATUS=1
fi



echo ""
echo ""
echo ""
exit $EXIT_STATUS
