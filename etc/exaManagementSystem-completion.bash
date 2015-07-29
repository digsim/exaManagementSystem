_exaManagementSystem()
{
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="--make-new-exercise --build-exam --build-all-exams --make-workbook --make-catalogue --preview-exercise --preview-solution --make-new-lecture"
    optssimple="-e -s -u -k -t -l"
    
    case "${prev}" in
        --make-new-lecture)
            local addopts="-l"
            COMPREPLY=( $(compgen -W "${addopts}" -- ${cur}) )
            return 0
            ;;
        --build-exam)
            local addopts="-s"
            COMPREPLY=( $(compgen -W "${addopts}" -- ${cur}) ) 
            return 0
            ;;
        --preview-exercise)
            local addopts="-e"
            COMPREPLY=( $(compgen -W "${addopts}" -- ${cur}) ) 
            return 0
            ;;
       --preview-solution)
            local addopts="-e"
            COMPREPLY=( $(compgen -W "${addopts}" -- ${cur}) ) 
            return 0
            ;;
       -s)
           local addopts=$(for x in `ls Exam_properties/ |awk -F "exam|.cfg" '{print $2}'|sort -g`; do echo ${x}; done)
           COMPREPLY=( $(compgen -W "${addopts}" -- ${cur}) ) 
           return 0
           ;;
       -e)
           local addopts=`ls Exercices/ |awk -F "ex" '{print $2}'| sed -e 's/\^\[\[0m\$//g'| sort -g | sed -r 's/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g' `
           COMPREPLY=( $(compgen -W "${addopts}" -- ${cur}) ) 
           return 0
           ;;
    esac
    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
    return 0
    
}
complete -F _exaManagementSystem exaManagementSystem
