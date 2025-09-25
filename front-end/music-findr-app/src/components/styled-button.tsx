import { LoadingOutlined } from "@ant-design/icons";
import React from "react";

interface StyledButtonProps {
  className?: string;
  htmlType?: "button" | "submit" | "reset";
  Icon?: React.FC;
  id?: string;
  size?: "small" | "normal" | "large";
  type: "primary" | "secondary" | "pay" | "branded";
  text?: string;
  disabled?: boolean;
  hidden?: boolean;
  onClick: () => void;
  onMouseEnter?: () => void;
  onMouseLeave?: () => void;
  onFocus?: () => void;
  loading?: boolean;
}

const StyledButton = ({
  className,
  htmlType = "button",
  Icon,
  id = "",
  size = "normal",
  text,
  type,
  disabled,
  hidden,
  onClick,
  onMouseEnter,
  onMouseLeave,
  onFocus,
  loading = false
}: StyledButtonProps) => {
  const defaultClassNames =
    "leading-none rounded-full transition-all duration-300";

  const sizeClassNames = (() => {
    switch (size) {
      case "small":
        return "px-3 py-1";

      case "normal":
        return "px-5 py-2";

      case "large":
        return "px-6 py-3";

      default:
        return "";
    }
  })();

  const typeClassNames = (() => {
    switch (type) {
      case "primary":
        return "text-white bg-portal-secondary hover:bg-portal-mainBlue";
      case "branded":
        return [
          "border",
          "bg-portal-branding-primary",
          "hover:bg-portal-branding-secondary",
          "text-portal-branding-text",
          "hover:text-portal-branding-textHover",
          "border-portal-branding-primary",
          "hover:border-portal-branding-secondary"
        ].join(" ");
      case "pay":
        return `text-gray-500 bg-portal-midGrey ${[
          "hover:text-portal-branding-text",
          "hover:bg-portal-branding-secondary"
        ].join(" ")}`;
      default:
        return "text-portal-primary border-portal-primary bg-transparent";
    }
  })();

  const disabledClass = (() => {
    if (disabled) {
      return "opacity-25 cursor-not-allowed";
    }
    return "cursor-pointer";
  })();

  return (
    <button
      id={id}
      type={htmlType}
      onClick={onClick}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
      onFocus={onFocus}
      className={`${defaultClassNames} ${typeClassNames} ${sizeClassNames} ${disabledClass} ${className}`}
      aria-label={text}
      disabled={disabled}
      hidden={hidden}
    >
      {loading ? (
        <LoadingOutlined />
      ) : (
        <>
          {Icon !== undefined && (
            <span className="inline-flex">
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