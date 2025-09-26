import { LoadingOutlined } from "@ant-design/icons";
import React from "react";

interface StyledButtonProps {
  className?: string;
  htmlType?: "button" | "submit" | "reset";
  Icon?: React.FC;
  id?: string;
  size?: "small" | "middle" | "large"; // aligned with AntD sizes
  type?: "primary" | "ghost" | "dashed" | "link" | "text" | "default";
  text?: string;
  disabled?: boolean;
  hidden?: boolean;
  onMouseEnter?: () => void;
  onMouseLeave?: () => void;
  onFocus?: () => void;
  loading?: boolean;
}

const StyledButton: React.FC<StyledButtonProps> = ({
  className,
  htmlType = "button",
  Icon,
  id = "",
  size = "middle",
  text,
  type = "default",
  disabled = false,
  hidden = false,
  onMouseEnter,
  onMouseLeave,
  onFocus,
  loading = false,
}) => {
  const defaultClassNames =
    "leading-none rounded-full transition-all duration-300";

  // Map AntD sizes to your padding classes
  const sizeClassNames =
    {
      small: "px-3 py-1",
      middle: "px-5 py-2",
      large: "px-6 py-3",
    }[size] || "";

  // Define your own styles or rely on AntD styles here
  const typeClassNames =
    {
      primary: "text-white bg-portal-secondary hover:bg-portal-mainBlue",
      ghost: "bg-transparent text-portal-primary hover:bg-gray-100",
      dashed:
        "border-dashed border-portal-primary text-portal-primary bg-transparent",
      link: "text-portal-primary underline hover:text-portal-mainBlue bg-transparent",
      text: "text-portal-primary bg-transparent hover:bg-gray-100",
      default:
        "text-portal-primary border border-portal-primary bg-transparent",
    }[type] || "";

  const disabledClass = disabled
    ? "opacity-25 cursor-not-allowed"
    : "cursor-pointer";

  const classes = [
    defaultClassNames,
    typeClassNames,
    sizeClassNames,
    disabledClass,
    className,
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <button
      id={id}
      type={htmlType}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
      onFocus={onFocus}
      className={classes}
      aria-label={text}
      disabled={disabled}
      hidden={hidden}
    >
      {loading ? (
        <LoadingOutlined />
      ) : (
        <>
          {Icon && (
            <span className="inline-flex mr-2">
              <Icon />
            </span>
          )}
          {text}
        </>
      )}
    </button>
  );
};

export default StyledButton;
