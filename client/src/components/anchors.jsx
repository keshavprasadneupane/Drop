export const NavigationAnchor = ({anchorName, navigateTo}) => {
    return <a href={navigateTo} className="font-poppins font-light cursor-pointer text-xl hover:text-blue-300 duration-400">{anchorName}</a>
}